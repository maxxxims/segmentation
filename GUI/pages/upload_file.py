from dash import Dash, dcc, html, Input, Output, State, callback, no_update
import plotly.express as px
import dash
from backend import Image, parse_json_file
import io
import json
from PIL import Image as IMG
import base64
import numpy as np


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash.register_page(__name__, path = '/upload_file')

next_step_button = {
    # 'display': 'none',
    'align': 'center',
}

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




def show_image(image_data, file_name: str):
    fig = px.imshow(image_data, binary_string=True, width=400, height=400)
    fig.update_layout(dragmode="drawclosedpath")
    return html.Div([
            html.H3('Uploaded image', style={'text-align': 'center'}),
            html.Div(children=[
                html.B(f'Filename: '), html.Span(file_name),
            ], style={'text-align': 'center'}),
            html.Div(
                [html.Img(src=IMG.fromarray(dash.get_app().image.data))], style={'display': 'flex',
                                                                                  'justify-content': 'center',
                                                                                  'margin-bottom': '20px'}
            )

        ], )


def load_image_from_png(content, filename):
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    img = Image(data=np.array(IMG.open(io.BytesIO(decoded))))
    dash.get_app().__setattr__('image', img)
    dash.get_app().__setattr__('json_data', {})


def load_image_from_json(content, filename):
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    data = json.loads(decoded)
    img = parse_json_file(data)
    dash.get_app().__setattr__('image', img)
    dash.get_app().__setattr__('json_data', data)


@callback(Output('output-image-upload-default', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def upload_file(content, file_name:str, list_of_dates):
    if content is not None:
        if file_name.endswith('.json'):
            load_image_from_json(content, file_name)
            dash.get_app().state_dict['start_annotation'] = False

        else:
            return html.Div([
                html.H3('Uploaded file should be in .json format', style={'text-align': 'center',
                                                                          'color': 'red'}),
            ])
        dash.get_app().__setattr__('last_figure', None)
        dash.get_app().__setattr__('markers_class_1', [])

    if hasattr(dash.get_app(), 'image'):
        next_step_button['display'] = 'block'
        if file_name is None and hasattr(dash.get_app(), 'json_data'):
            file_name = dash.get_app().json_data['image_tag'] + '.json'
        return show_image(dash.get_app().image.data, file_name)#, next_step_button
    
    return no_update