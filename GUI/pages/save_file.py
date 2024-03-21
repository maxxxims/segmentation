import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update, callback, State
from skimage import data
import json
import matplotlib.pyplot as plt
import dash
from PIL import Image as IMG
from backend import Image, draw_annotations, save_annotation, check_annotation, draw_annotated_image
import numpy as np
from GUI.database import session_table, image_table, figure_table
from GUI.utils import login_required
from flask import request
from pathlib import Path


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
def layout():
    layout = html.Div(
        [   
            html.Div(
                id='text-under-button',
                children=[html.B(children="Marked segments: "),
                        html.Span(children=DEFAULT_MARKED_SEGMENTS, id="text-marked-segments-2"),
                        html.Br(),
                        html.Div(
                            [
                                html.Button("SAVE IMAGE", id="button-save-annotated-img", n_clicks=0, style={'width': '10%'}),
                                html.Button("CHECK ANNOTATION", id="button-check-annotated-img", 
                                n_clicks=0, style = {'display': 'none', 'width': '10%', 'margin-left': '40px'}),
                            ], style={'display': 'flex', 'margin-top': '15px'},
                    
                        ),
                        html.P(children=[
                            html.B('Saved path: '), html.Span(id='text-save-annotated-img', children='not saved yet')
                        ]),
                        # html.P(id='container-result-annotated-img', children=[]),
                        html.P(children=[
                            html.B('Accuracy:   '), html.Span(id='result-accuracy', children=DEFAULT_ACCURACY)
                        ]),
                        #html.Div(id='text-save-annotated-img', children='', style={'line-height': '1.5'}),
                        html.Div(id='container-result-annotated-img', children=[])

                        ],
                        
                style={'margin-left': '5%', 'font-size': '20px', 'line-height': '0.8'}
            ),
            
            html.Button("Load polygons", id="button-img-show-polygons", n_clicks=0, style={'display': 'none'}),

            
            html.Div(id="container-img-annotated", children=[
                dcc.Graph(id="graph-pic-annotated", figure=default_figure, config=config),
                dcc.Markdown("Characteristics of shapes"),
                html.Pre(id="annotations-data-pre"),

            ]),
            
        ]
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
    print(f'username = {username} - {n_clicks}')
    last_figure = figure_table.get_last_figure(username=username)
    if last_figure is not None:
        marker_class_1 = figure_table.get_marker_class_1(username=username)
        img = image_table.get_image(username=username)
        selected_class = session_table.get_selected_class(username=username)
        img_annotated = draw_annotated_image(_img=img, data=marker_class_1, selected_class=selected_class)
        fig = px.imshow(img_annotated, binary_string=True, width=800, height=800)
        fig.update_layout(dragmode="drawclosedpath")
        return fig, len(marker_class_1)
    else:
        global DEFAULT_ACCURACY
        DEFAULT_ACCURACY = 'not checked yet'
    return default_figure, DEFAULT_MARKED_SEGMENTS
        
    

@callback(
    Output('text-save-annotated-img', 'children'),
    Output('button-check-annotated-img', 'style'),
    Input("button-save-annotated-img", "n_clicks"),
    prevent_initial_call=True
)
@login_required
def save_annotated_img(n_clicks, username):
    marker_class_1 = figure_table.get_marker_class_1(username=username)
    last_figure = figure_table.get_last_figure(username=username)
    
    if marker_class_1 is None or last_figure is None:
        buttons_syles['display'] = 'none'
        return "annotations not found", buttons_syles
    
    img = image_table.get_image(username=username)
    json_data = figure_table.get_json_data(username=username)
    
    path_to_save = save_annotation(img=img, data=marker_class_1,
                    data_json=json_data)
    
    session_table.update_save_path(username=username, save_path=str(path_to_save))
    buttons_syles['display'] = 'block'
    return f'{path_to_save}', buttons_syles

"""

"""

@callback(
    Output('container-result-annotated-img', 'children'),
    Output('result-accuracy', 'children'),
    Input("button-check-annotated-img", "n_clicks"),
    prevent_initial_call=True
)
@login_required
def check_annotation_img(n_clicks, username):
    global DEFAULT_ACCURACY
    json_data = figure_table.get_json_data(username=username)
    if json_data is not None:
        if n_clicks > 0 and n_clicks %2 == 0:
            return html.Div(), DEFAULT_ACCURACY
        
        marker_class_1 = figure_table.get_marker_class_1(username=username)
        selected_class = session_table.get_selected_class(username=username)
        path_to_save = session_table.get_save_path(username=username)
        n_segments = -1
        if marker_class_1 is not None:
            n_segments = len(marker_class_1)

        metrics, img = check_annotation(json_data, selected_color=selected_class,
                                        save_acc=True, path_to_save=path_to_save,
                                        n_segments=n_segments)
        
        # print(f'ACCURACY = {metrics}')
        DEFAULT_ACCURACY = metrics['Accuracy']
        fig = px.imshow(img.data, binary_string=True, width=800, height=800)
        return html.Div(
            [
                # html.H3(f"Accuracy = {metrics['Accuracy']}"),
                html.P("""In the image below the same as you've saved now.
                        To remove this image, click again "CHEK ANNOTATION" """),
                dcc.Graph(figure=fig)
            ]
        ), metrics['Accuracy']
    
    else:
        return html.H4("Image wasn't loaded from json", style={'color': 'red'}), DEFAULT_ACCURACY
