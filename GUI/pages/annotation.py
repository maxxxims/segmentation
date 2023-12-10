import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update, callback, State, ctx
from skimage import data
import json
import matplotlib.pyplot as plt
import dash
from PIL import Image as IMG
from backend import Image
import numpy as np

dash.register_page(__name__, path = '/annotation')



default_figure = 255 * np.ones((200, 200, 3))

fig = px.imshow(default_figure, binary_string=True, width=800, height=800)
fig.update_layout(dragmode="drawclosedpath")

config = {
    "modeBarButtonsToAdd": [
        # "drawline",
        "drawopenpath",
        "drawclosedpath",
        # "drawcircle",
        # "drawrect",
        "eraseshape",
    ]
}

# Build App
layout = html.Div(
    [   
        html.Div(
            id='text-under-button',
            children=[html.B(children="Marked segments: "),
                      html.Span(children='0', id="text-marked-segments"),
                      ],
            style={'margin-left': '5%', 'font-size': '20px', 'width': '25%'}
        ),
        html.Button("Show image", id="button-img-show", n_clicks=0, style={'display': 'none'}),

        html.Div(id="container-img", children=[   #style={'widhth': '800px', 'height': 'auto'},
            dcc.Graph(id="graph-pic", figure=fig, config=config, style={'align': 'center'}),
            # dcc.Markdown("Characteristics of shapes"),
            html.Pre(id="annotations-data-pre"),

        ]),
        
        html.Div(id='container-slider-img-size', children=[
            html.P('Set image size'),
            dcc.Slider(100, 2000, marks=None, value=200, id='slider-img-size'),
        ], style={'margin-left': '5%', 'font-size': '20px', 'width': '25%'})
        
    ]
)


@callback(
    Output('graph-pic', 'figure'),
    Input('button-img-show', 'n_clicks'),
    State("graph-pic", "figure"),
    Input("slider-img-size", "value"),
    # prevent_initial_call=True
)
def show_image(n_clicks, figure, slider_value):
    
    # if ctx.triggered_id == 'slider-img-size' and hasattr(dash.get_app(), 'last_figure'):
    #     print(dash.get_app().last_figure.keys())
    #     fig = px.imshow(dash.get_app().image.data, binary_string=True, width=slider_value)#, height=800)
    #     fig.update_layout(dragmode="drawclosedpath")
    #     return fig
    if hasattr(dash.get_app(), 'image'):
        if dash.get_app().last_figure is not None:
            return dash.get_app().last_figure
        fig = px.imshow(dash.get_app().image.data, binary_string=True, width=slider_value)#, height=800)
        fig.update_layout(dragmode="drawclosedpath")
        return fig
        
    else:
        return no_update

# from pprint import pprint

@callback(
    # Output("annotations-data-pre", "children"),
    Output('text-marked-segments', 'children'),
    Input("graph-pic", "relayoutData"),
    State("graph-pic", "figure"),
    # prevent_initial_call=True,
)
def on_new_annotation(relayout_data, figure):
    if relayout_data is not None:
        if "shapes" in relayout_data and hasattr(dash.get_app(), 'image'):
            dash.get_app().__setattr__('last_figure', figure)
            makrers_data = relayout_data["shapes"] 
            if not hasattr(dash.get_app(), 'markers_class_1'):
                dash.get_app().__setattr__('markers_class_1', None)
            dash.get_app().markers_class_1 = makrers_data

            # pprint(dash.get_app().markers_class_1)

    # return number of marked segments
    if hasattr(dash.get_app(), 'markers_class_1') and dash.get_app().last_figure is not None:
        return len(dash.get_app().markers_class_1)
    else:
        return 0
    
"""


@callback(
    Output('graph-pic', 'figure'),
    Output('text-marked-segments', 'children'),
    Input('button-img-show', 'n_clicks'),
    # Input("slider-img-size", "value"),
    Input("graph-pic", "relayoutData"),
    State("graph-pic", "figure"),
    # prevent_initial_call=True
)
def graph_control(n_clicks, relayout_data, figure):
    n_marked_classes = 0
    if hasattr(dash.get_app(), 'markers_class_1') and dash.get_app().last_figure is not None:
        n_marked_classes = len(dash.get_app().markers_class_1)


    if relayout_data is not None:
        if "shapes" in relayout_data and hasattr(dash.get_app(), 'image'):
            dash.get_app().__setattr__('last_figure', figure)
            makrers_data = relayout_data["shapes"] 
            if not hasattr(dash.get_app(), 'markers_class_1'):
                dash.get_app().__setattr__('markers_class_1', None)
            dash.get_app().markers_class_1 = makrers_data

    if hasattr(dash.get_app(), 'last_figure'):
        if dash.get_app().last_figure is not None:
            return dash.get_app().last_figure, n_marked_classes
    fig = px.imshow(dash.get_app().image.data, binary_string=True)
    fig.update_layout(dragmode="drawclosedpath")
    return  fig, n_marked_classes

# Решить проблему с обновлением фигур
"""