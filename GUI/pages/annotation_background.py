import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update, callback, State
from skimage import data
import json
import matplotlib.pyplot as plt
import dash
from PIL import Image as IMG
from backend import Image, draw_annotations, save_annotation, check_annotation, draw_annotated_image
import numpy as np

dash.register_page(__name__, path = '/annotation_background')


default_figure = 255 * np.ones((200, 200, 3))
default_figure = px.imshow(default_figure, binary_string=True, width=800, height=800)
default_figure.update_layout(dragmode="drawclosedpath")

DEFAULT_ACCURACY = 'not checked yet'
DEFAULT_MARKED_SEGMENTS = 'annotations not found'

buttons_syles = {
    'width': '10%',
    'margin-left': '40px',
}

config = {
    "modeBarButtonsToAdd": [
        # "drawline",
        # "drawopenpath",
        # "drawclosedpath",
        # "drawcircle",
        # "drawrect",
        # "eraseshape",
    ]
}

# Build App
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




@callback(
    Output('graph-pic-annotated', 'figure'),
    Output('text-marked-segments-2', 'children'),
    Input('button-img-show-polygons', 'n_clicks'),
    State("graph-pic-annotated", "figure"),
)
def show_image(n_clicks, figure):
    if hasattr(dash.get_app(), 'last_figure'):
        if dash.get_app().last_figure is not None:
            data = dash.get_app().markers_class_1
            # img_annotated, img = draw_annotations(_img=dash.get_app().image.data, data=data, reverse=True)
            img_annotated = draw_annotated_image(_img=dash.get_app().image.data, data=data, selected_class=dash.get_app().state_dict['selected_class'])
            fig = px.imshow(img_annotated, binary_string=True, width=800, height=800)
            fig.update_layout(dragmode="drawclosedpath")
            return fig, len(dash.get_app().markers_class_1)
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
def save_annotated_img(n_clicks):
    if not hasattr(dash.get_app(), 'markers_class_1'):
        buttons_syles['display'] = 'none'
        return "annotations not found", buttons_syles
    
    if hasattr(dash.get_app(), 'last_figure'):
        if dash.get_app().last_figure is None:
            buttons_syles['display'] = 'none'
            return "annotations not found", buttons_syles
        
    path_to_save = save_annotation(img=dash.get_app().image.data, data=dash.get_app().markers_class_1,
                    data_json=dash.get_app().json_data)
    dash.get_app().__setattr__('path_to_save', path_to_save)
    buttons_syles['display'] = 'block'
    return f'{path_to_save}', buttons_syles



@callback(
    Output('container-result-annotated-img', 'children'),
    Output('result-accuracy', 'children'),
    Input("button-check-annotated-img", "n_clicks"),
    prevent_initial_call=True
)
def check_annotation_img(n_clicks):
    global DEFAULT_ACCURACY
    if hasattr(dash.get_app(), 'json_data'):

        if n_clicks > 0 and n_clicks %2 == 0:
            return html.Div(), DEFAULT_ACCURACY
        
        n_segments = -1
        if hasattr(dash.get_app(), 'markers_class_1'):
            n_segments = len(dash.get_app().markers_class_1)

        metrics, img = check_annotation(dash.get_app().json_data, selected_color=dash.get_app().state_dict['selected_class'],
                                        save_acc=True, path_to_save=dash.get_app().path_to_save,
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
    