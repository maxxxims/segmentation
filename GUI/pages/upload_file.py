from dash import Dash, dcc, html, Input, Output, State, callback, no_update
import plotly.express as px
import dash
from backend import Image, parse_json_file
import io
import json
from PIL import Image as IMG
import base64
import numpy as np
from matplotlib import pyplot as plt
from GUI.database import session_table, image_table, figure_table
from GUI.utils import login_required
from flask import request


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash.register_page(__name__, path = '/upload_file')

next_step_button = {
    'align': 'center',
}


def layout():
    layout = html.Div([
        html.Div(id='output-image-upload-default'),
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                # 'margin': '10px',
            },
            multiple=False
        ),
        html.Button(id='hidden-button', style={'display': 'none'}),
        html.Div(id='output-image-upload'),
    ], style = {
                'alignContnent': 'center',
                'align': 'center',
                'postion': 'absolute',
    })
    return layout



def show_image(username: str, file_name: str):
    image_data = image_table.get_image(username)
    #fig = px.imshow(image_data, binary_string=True, width=400, height=400)
    #fig.update_layout(dragmode="drawclosedpath")
    return html.Div([
            html.H3('Uploaded image', style={'text-align': 'center'}),
            html.Div(children=[
                html.B(f'Filename: '), html.Span(file_name),
            ], style={'text-align': 'center'}),
            html.Div(
                [html.Img(src=IMG.fromarray(image_data))], style={'display': 'flex',
                                                                                  'justify-content': 'center',
                                                                                  'margin-bottom': '20px'}
            )

        ], )


"""def load_image_from_png(content, filename):
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    img = Image(data=np.array(IMG.open(io.BytesIO(decoded))))
    dash.get_app().__setattr__('image', img)
    dash.get_app().__setattr__('json_data', {})"""


def load_image_from_json(content, filename, username: str):
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    data = json.loads(decoded)
    img = parse_json_file(data, test=True)
    image_table.save_image(username, img)
    session_table.update_loaded_image(username=username, loaded_image=True)
    figure_table.save_json_data(username=username, json_data=data)


@callback(Output('output-image-upload-default', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
@login_required
def upload_file(content, file_name:str, list_of_dates, username):
    if content is not None:
        if file_name.endswith('.json'):
            load_image_from_json(content, file_name, username)
            session_table.update_start_annotation(username=username, start_annotation=False)
        else:
            return html.Div([
                html.H3('Uploaded file should be in .json format', style={'text-align': 'center',
                                                                          'color': 'red'}),
            ])
        figure_table.delete_last_figure(username=username)
        figure_table.delete_marker_class_1(username=username)


    if session_table.is_loaded_image(username):
        next_step_button['display'] = 'block'
        if file_name is None:
            json_data = figure_table.get_json_data(username=username)
            file_name = json_data['image_tag'] + '.json'
        return show_image(username, file_name)
    return no_update