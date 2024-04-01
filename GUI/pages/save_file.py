import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update, callback, State
from skimage import data
import json
import matplotlib.pyplot as plt
import dash
from PIL import Image as IMG
from backend import Image, draw_annotations, save_annotation, check_annotation, draw_annotated_image
import numpy as np
from GUI.database import session_table, image_table, figure_table, user2task_table
from GUI.utils import login_required, finish_task
from flask import request
from pathlib import Path
import dash_bootstrap_components as dbc


dash.register_page(__name__, path = '/annotation_background')


default_figure = 255 * np.ones((200, 200, 3))
default_figure = px.imshow(default_figure, binary_string=True, width=800, height=800)
# default_figure.update_layout(dragmode="drawclosedpath")

DEFAULT_ACCURACY = 'not checked yet'
DEFAULT_MARKED_SEGMENTS = 'annotations not found'

buttons_syles = {
    'width': '10%',
    'margin-left': '40px',
}

config = {
    "modeBarButtonsToAdd": [
    ]
}

# Build App
@login_required
def layout(username):
    acccuracy = DEFAULT_ACCURACY
    current_task_uuid = user2task_table.get_current_task_uuid(username=username)
    if current_task_uuid is not None:
        acccuracy = user2task_table.get_metric(uuid=current_task_uuid)
        if acccuracy is not None:   acccuracy = round(acccuracy, 4)
        else:   acccuracy = DEFAULT_ACCURACY
    layout = html.Div(
        [   
            html.Div(
                id='text-under-button',
                children=[html.B(children="Marked segments: "),
                        html.Span(children=DEFAULT_MARKED_SEGMENTS, id="text-marked-segments-2"),
                        html.Br(),
            
                        html.P(children=[
                            html.B('Accuracy:   '), html.Span(id='result-accuracy', children=acccuracy),
                            html.Br(),
                            html.P(id='low-accuracy-msg', style={'color': 'red'}),
                        ]),
                        html.Div(
                            [
                                dbc.Button("SAVE IMAGE", id="button-save-annotated-img", n_clicks=0, style={'width': '10%'}, color="success", className="me-1"),
                            ], style={'display': 'flex', 'margin-top': '15px'},
                    
                        ),
                        html.Div(id='container-result-annotated-img', children=[])

                        ],
                        
                style={'margin-left': '5%', 'font-size': '20px', }#'line-height': '0.8'
            ),

            
            html.Center(id="container-img-annotated", children=[
                dcc.Graph(id="graph-pic-annotated", figure=default_figure, config=config),
                html.Pre(id="annotations-data-pre"),

            ], style={'justify-content': 'center'},
                     ),
            html.Button(id='button-img-show-polygons', hidden=True)
            
        ], style={'justify-content': 'center'},
    )
    return layout



@callback(
    Output('graph-pic-annotated', 'figure'),
    Output('text-marked-segments-2', 'children'),
    Input('button-img-show-polygons', 'n_clicks'),
    State("graph-pic-annotated", "figure"),
)
@login_required
def show_image(n_clicks, figure, username):
    #print(f'username = {username} - {n_clicks}')
    last_figure = figure_table.get_last_figure(username=username)
    print(f'LAST FIGURE IS NONE ={last_figure is None} FROM USER = {username}')
    if last_figure is not None:
        marker_class_1 = figure_table.get_marker_class_1(username=username)
        img = image_table.get_image(username=username)
        selected_class = session_table.get_selected_class(username=username)
        json_data = figure_table.get_json_data(username=username)
        img_annotated = draw_annotated_image(_img=img, data=marker_class_1, selected_class=selected_class, json_data=json_data)
        fig = px.imshow(img_annotated, binary_string=True, width=800, height=800)
        fig.update_layout(dragmode="drawclosedpath")
        return fig, len(marker_class_1)
    else:
        global DEFAULT_ACCURACY
        DEFAULT_ACCURACY = 'not checked yet'
    return default_figure, DEFAULT_MARKED_SEGMENTS
        
    

@callback(
    Output('result-accuracy', 'children'),
    Output('low-accuracy-msg', 'children'),
    Input("button-save-annotated-img", "n_clicks"),
    running=[(Output("button-save-annotated-img", "disabled"), True, False)],
    prevent_initial_call=True
)
@login_required
def save_annotated_img(n_clicks, username):
    task_uuid = user2task_table.get_current_task_uuid(username=username)
    marker_class_1 = figure_table.get_marker_class_1(username=username)
    last_figure = figure_table.get_last_figure(username=username)
    selected_class = session_table.get_selected_class(username=username)
    
    if marker_class_1 is None or last_figure is None:
        buttons_syles['display'] = 'none'
        return "not checked yet", no_update
    
    img = image_table.get_image(username=username)
    json_data = figure_table.get_json_data(username=username)
    attempt_number = user2task_table.get_current_task_attempt_number(username=username)
    current_task = user2task_table.get_task_by_uuid(uuid=task_uuid)
    
    path_to_save_folder = Path('data/output') / username
    # path_to_save_folder.mkdir(parents=True, exist_ok=True)
    image_name = current_task.image_name
    folder_name = f'{image_name}_{attempt_number}'
    
    """"""
    #SAVE ANNOTATION
    annotated_image = draw_annotated_image(_img=img, data=marker_class_1, selected_class=selected_class, json_data=json_data)
    path_to_save, data_json = save_annotation(annotated_image=annotated_image, data=marker_class_1,
                    data_json=json_data, path_to_save=path_to_save_folder, folder_name=folder_name)
    
    # CALCULATE ACCUARACY
    accuracy, gt_img = check_annotation(json_data, annotated_image)
    json_data['accuracy'] = accuracy
    """"""
    
    figure_table.save_json_data(username=username, json_data=data_json)
    user2task_table.update_metric(task_uuid, metric=accuracy)    
    user2task_table.update_save_folder(username=username, uuid=task_uuid, save_folder=str(path_to_save_folder))
    session_table.update_save_path(username=username, save_path=str(path_to_save))
    user2task_table.update_finished(username=username, uuid=task_uuid, finished=True)
    #finish_task(username)

    if accuracy < 0.8:
        return round(accuracy, 4), f'Low accuracy, please try again. Maybe you have chosen wrong class. It can be changed on the Annotation page'
    return round(accuracy, 4), no_update    

"""

"""