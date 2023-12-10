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
    # html.Button(id='button-next-step1', style=next_step_button,
    #             children=[html.A("NEXT_STEP", href='/annotation')]),

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





# def parse_contents(contents, filename, date):
#     return html.Div([
#         html.H5(filename),
#         html.H6(datetime.datetime.fromtimestamp(date)),

#         # HTML images accept base64 encoded strings in the same format
#         # that is supplied by the upload
#         html.Img(src=contents, style={'height': '50%', 'width': 'auto', 'align': 'center'}),
#         html.Hr(),
#         html.Div('Raw Content'),
#         html.Pre(contents[0:200] + '...', style={
#             'whiteSpace': 'pre-wrap',
#             'wordBreak': 'break-all'
#         })
#     ])

def show_image(image_data):
    fig = px.imshow(image_data, binary_string=True, width=400, height=400)
    fig.update_layout(dragmode="drawclosedpath")
    return html.Div([
            html.H3('Uploaded image', style={'text-align': 'center'}),
            html.Div(
                [html.Img(src=IMG.fromarray(dash.get_app().image.data))], style={'display': 'flex',
                                                                                  'justify-content': 'center',
                                                                                  'margin-bottom': '20px'}
            )
            # dcc.Graph(id="graph-pic", figure=fig, style={'align': 'center'})
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

        else:
            return html.Div([
                html.H3('Uploaded file should be in .json format', style={'text-align': 'center',
                                                                          'color': 'red'}),
            ])

        dash.get_app().__setattr__('last_figure', None)
        


    if hasattr(dash.get_app(), 'image'):
        next_step_button['display'] = 'block'
        return show_image(dash.get_app().image.data)#, next_step_button
    
    return no_update