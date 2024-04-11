import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update, callback, State
from skimage import data
import json
import matplotlib.pyplot as plt
import dash
from PIL import Image as IMG
from backend import Image, draw_annotations, save_annotation, check_annotation, draw_annotated_image, \
    draw_polygons_on_last_figure
import numpy as np
from GUI.database import session_table, image_table, figure_table, user2task_table
from GUI.utils import login_required, finish_task, validate_pixels_propotions, calculate_pixels_proportions
from flask import request
from pathlib import Path
import dash_bootstrap_components as dbc
import logging


dash.register_page(__name__, path = '/annotation_background')


default_figure = 255 * np.zeros((300, 300, 3))
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
square_size = 20
BLACK_SQUARE = html.Div(style={'background-color': 'black', 'width': square_size, 'height': square_size, 'display': 'inline-block', 'border': 'black'})
WHITE_SQUARE = html.Div(style={'background-color': 'white', 'width': square_size, 'height': square_size, 'border': '2px solid black', 'display': 'inline-block'})
GRAY_SQUARE = html.Div(style={'background-color': 'rgb(128, 128, 128)', 'width': square_size, 'height': square_size, 'border': '2px solid black', 'display': 'inline-block'})

# Build App
@login_required
def layout(username):
    acccuracy = DEFAULT_ACCURACY
    current_task_uuid = user2task_table.get_current_task_uuid(username=username)
    if current_task_uuid is not None:
        acccuracy = user2task_table.get_metric(uuid=current_task_uuid)
        if acccuracy is not None:   acccuracy = round(acccuracy, 4)
        else:   acccuracy = DEFAULT_ACCURACY
    
    classes_info = html.Div(children=[
        html.Span(children=[
            WHITE_SQUARE, html.B(' Class 1:   '), html.Span(id='result-class-1', children=''), #dbc.Progress(id='progress-1', value=0, striped=True, hi)
        ]), html.Br(),
        html.Span(children=[
            GRAY_SQUARE, html.B(' Class 0:   '), html.Span(id='result-class-0', children=''),
        ]), html.Br(),
        html.Span([
            BLACK_SQUARE, html.B(' Unmarked'),
        ])
        #html.Span('Class 1: '), WHITE_SQUARE, html.Span(' Class 0: '), GRAY_SQUARE, html.Span(' Unmarked: '), BLACK_SQUARE
    ])    
    
    col1 = dbc.Col([
        html.B(children="Marked segments: "),
        html.Span(children=DEFAULT_MARKED_SEGMENTS, id="text-marked-segments-2"),
        html.Br(),
        html.P(children=[
            html.B('Accuracy:   '), html.Span(id='result-accuracy', children=acccuracy),
            html.Br(),
            html.P(id='low-accuracy-msg', style={'color': 'red'}),
        ]),
        html.Div(
            [
                dbc.Button("SAVE IMAGE", id="button-save-annotated-img", n_clicks=0, color="success", className="me-1", disabled=True), #style={'width': '10%'}
            ], style={'display': 'flex', 'margin-top': '15px'},
    
        ),
    ])
    
    col2 = dbc.Col([
        classes_info, 
    ])
    
    col21 = dbc.Col([
        html.P(children=[
            html.Span('One or more classes are not fully annotated, please retry.', hidden=True, id='bad-annotation-msg', style={'color': 'red'}),
        ])
    ])
    
    top_panel = html.Div([
        dbc.Row([col1, col2], ),
        html.Br(),
        dbc.Row([col21]),
        ], style={'margin-left': '5%', 'font-size': '20px', })
    
    layout = html.Div(
        [   
            top_panel,
            
            html.Center(id="container-img-annotated", children=[
                dcc.Graph(id="graph-pic-annotated", figure=default_figure, config=config),
                html.Pre(id="annotations-data-pre"),

            ], style={'justify-content': 'center'},
                     ),
            html.Button(id='button-img-show-polygons', hidden=True),
            html.Button(id='hidden-id', hidden=True, ),
        ], style={'justify-content': 'center'},
    )
    return layout

@callback(
    Output('result-class-1', 'children'),
    Output('result-class-0', 'children'),
    Output('bad-annotation-msg', 'hidden'),
    Output("button-save-annotated-img", "disabled"),
    Input('hidden-id', 'n_clicks'),
)
@login_required
def annotation_info(n_clicks, username: str):
    last_figure = figure_table.get_last_figure(username=username)
    img = image_table.get_image(username=username)
    marker_class_1 = figure_table.get_marker_class_1(username=username)
    if marker_class_1 is None or last_figure is None or img is None:
        return no_update, no_update, True, True 
    
    json_data = figure_table.get_json_data(username=username)
    _, annotation_info = draw_polygons_on_last_figure(last_figure, img, marker_class_1, 0.8, return_annotation_info=True, json_data=json_data)
    class_1 = annotation_info['class_1']
    class_0 = annotation_info['class_0']
    
    class_1, class_0 = calculate_pixels_proportions(username, class_1, class_0, to_str=False)
    validate_annotation = validate_pixels_propotions(class_1, class_0)
    class_1, class_0 = f"{class_1}%", f"{class_0}%"
    if not validate_annotation:
        return class_1, class_0, False, True
    return class_1, class_0, True, False
    


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
    logging.info(f'LAST FIGURE IS NONE ={last_figure is None} FROM USER = {username}')
    # print(f'LAST FIGURE IS NONE ={last_figure is None} FROM USER = {username}')
    if last_figure is not None:
        marker_class_1 = figure_table.get_marker_class_1(username=username)
        img = image_table.get_image(username=username)
        json_data = figure_table.get_json_data(username=username)
        img_annotated = draw_annotated_image(_img=img, data=marker_class_1, json_data=json_data)
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
    annotated_image = draw_annotated_image(_img=img, data=marker_class_1, json_data=json_data)
    
    # CALCULATE ACCUARACY
    accuracy = check_annotation(json_data, annotated_image)
    json_data['accuracy'] = accuracy
    
    
    path_to_save, data_json = save_annotation(annotated_image=annotated_image, data=marker_class_1,
                    data_json=json_data, path_to_save=path_to_save_folder, folder_name=folder_name)
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