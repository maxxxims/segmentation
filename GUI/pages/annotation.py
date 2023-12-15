import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update, callback, State, ctx
from skimage import data
import json
import matplotlib.pyplot as plt
import dash
from PIL import Image as IMG
from backend import Image
import numpy as np
from backend import draw_annotations


dash.register_page(__name__, path = '/annotation')


NEWSHAPE = {'opacity': 0.6, 'fillrule':'evenodd',
             'line': {'color': 'red','dash': 'solid'}}

WARNING_MSG_CHANGE_SELECTOR = 'Sorry, you can change this before annotating. Reload the image'

def get_figure(img_data, height=800):
    fig = px.imshow(default_figure, binary_string=True, height=height)
    # fig.update_layout(dragmode="drawopenpath",
    #                   newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="darkblue", width=8)))
    # nonzero
    fig.update_layout(dragmode="drawopenpath", 
                    newshape=NEWSHAPE)
    
    return fig


def get_options():
    return [
        {'label': 'class 1',    'value': 1},
        {'label': 'background 0', 'value': 0},
    ]


default_figure = 255 * np.ones((200, 200, 3))

fig = get_figure(default_figure)


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


layout = html.Div(
    [   
        html.Div(
            id='text-under-button',
            children=[html.B(children="Marked segments: "),
                      html.Span(children='0', id="text-marked-segments"), html.Br(),
                      html.B(children="Selected class: "),
                      html.Span(children='', id="text-selected-class"),
                      dcc.Dropdown(
                          id="dropdown-selected-class",
                          options=get_options()
                      ),
                      
                      #html.Button("Change class", id="button-img-change-class", n_clicks=0, style={'margin-left': '5%'}),
                      html.Span(children='', id='warning-msg-selector', style={'color': 'red'}),
                      ],
            style={'margin-left': '5%', 'font-size': '20px', 'width': '25%'}
        ),
        html.Button("Show image", id="button-img-show", n_clicks=0, style={'display': 'none'}),

        html.Div(id="container-img", children=[   #style={'widhth': '800px', 'height': 'auto'},
            dcc.Graph(id="graph-pic", figure=fig, config=config, ),
            html.Div(
                style={'justify-content': 'center'},
                children=[
                    html.Button(children="Fill Background", id="button-img-fill-bg", n_clicks=0, style={ 'align': 'center'}),
                    html.Button(children="Fill Class 1", id="button-img-fill-class-1", n_clicks=0, style={ 'align': 'center'}),
                    html.H3('Annotated Image Preview', style={'text-align': 'center'}),
                ]
            ),
            
            dcc.Graph(id="preview-annotated", figure=fig, config={}),
            html.Pre(id="annotations-data-pre"),

        ]), #'justify-content': 'center', 'margin-bottom': '20px' style={'display': 'flex', }
        

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
        fig = px.imshow(dash.get_app().image.data, binary_string=True, width=800)#, height=800)
        fig.update_layout(dragmode="drawopenpath", 
                    newshape=NEWSHAPE)
        
        return fig
        
    else:
        return no_update



@callback(
    Output('text-marked-segments', 'children'),
    Input("graph-pic", "relayoutData"),
    State("graph-pic", "figure"),
    
)
def on_new_annotation(relayout_data, figure):
    # add annotations
    if relayout_data is not None:
        if "shapes" in relayout_data and hasattr(dash.get_app(), 'image'):
            dash.get_app().state_dict['start_annotation'] = True    # start annotating
            dash.get_app().__setattr__('last_figure', figure)
            makrers_data = relayout_data["shapes"] 
            if not hasattr(dash.get_app(), 'markers_class_1'):
                dash.get_app().__setattr__('markers_class_1', None)
            dash.get_app().markers_class_1 = makrers_data


    # return number of marked segments
    if hasattr(dash.get_app(), 'markers_class_1') and dash.get_app().last_figure is not None:
        return len(dash.get_app().markers_class_1)
    else:
        return 0
    

@callback(
    Output('dropdown-selected-class', 'options'),
    Output('text-selected-class', 'children'),
    Output('warning-msg-selector', 'children'),
    Input('dropdown-selected-class', 'value'),
)
def change_selected_class(value):
    # change options if start annotating
    if dash.get_app().state_dict.get('start_annotation', False):
        options = get_options()
        for option in options:
            option['disabled'] = True
        if ctx.triggered_id is None:
            warning_msg = ''
        else:
            warning_msg = WARNING_MSG_CHANGE_SELECTOR
    else:
        if value is not None:
            dash.get_app().state_dict['selected_class'] = value
        options = no_update
        warning_msg = ''
    return options, dash.get_app().state_dict['selected_class'], warning_msg



@callback(
    Output('preview-annotated', 'figure'),
    Input('button-img-fill-bg', 'n_clicks'),
    Input('button-img-fill-class-1', 'n_clicks'),
)
def show_preview(n_clicks1, n_clicks2):
    if hasattr(dash.get_app(), 'image') and hasattr(dash.get_app(), 'markers_class_1'):
        reverse = False
        if ctx.triggered_id == 'button-img-fill-class-1':
            if dash.get_app().state_dict['selected_class'] == '1':
                reverse = False
            else:
                reverse = True
        elif ctx.triggered_id == 'button-img-fill-bg':
            if dash.get_app().state_dict['selected_class'] == '1':
                reverse = True
            else:
                reverse = False


        img_add, img = draw_annotations(dash.get_app().image.data, dash.get_app().markers_class_1, reverse=reverse)
        fig = px.imshow(img_add, binary_string=True, width=800, height=800)

        return fig
    else:
        return no_update
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