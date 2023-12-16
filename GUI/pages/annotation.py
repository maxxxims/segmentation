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
                      
                    #   html.Button("load img =", id="button-load-img", n_clicks=0, style={'margin-left': '5%'}),
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
            if int(dash.get_app().state_dict['selected_class']) == 1:
                reverse = False
            else:
                reverse = True
        elif ctx.triggered_id == 'button-img-fill-bg':
            if int(dash.get_app().state_dict['selected_class']) == 1:
                reverse = True
            else:
                reverse = False


        img_add, img = draw_annotations(dash.get_app().image.data, dash.get_app().markers_class_1, reverse=reverse)
        fig = px.imshow(img_add, binary_string=True, width=800, height=800)
        # print()
        return fig
    else:
        return no_update
    



@callback(
    Output('graph-pic', 'figure'),
    Output('text-marked-segments', 'children'),
    Input("graph-pic", "relayoutData"),
    State("graph-pic", "figure"),
    # prevent_initial_call=True
    
)
def on_new_annotation(relayout_data,figure):
    # print(figure.keys(), type(figure['data'][0]['source']), figure['data'][0].keys())
    # # print((figure['data'][0]['source']))
    # import base64
    # decoded = base64.b64decode(figure['data'][0]['source'].split(',')[1])
    # print(list(decoded))
    # print()


    # initial call
    if ctx.triggered_id is None:
        if not hasattr(dash.get_app(), 'image'):
            return get_figure(default_figure), 0
        if dash.get_app().last_figure is not None:
            return dash.get_app().last_figure, 0
        if dash.get_app().last_figure is None and hasattr(dash.get_app(), 'image'):
            fig = px.imshow(dash.get_app().image.data, binary_string=True, width=800)#, height=800)
            fig.update_layout(dragmode="drawopenpath", 
                        newshape=NEWSHAPE)
            dash.get_app().__setattr__('markers_class_1', [])
            return fig, 0
        print('Situation unexpected.')
        return get_figure(default_figure), 0
    
    print(relayout_data)
    if relayout_data is not None and hasattr(dash.get_app(), 'image'):
        resize_arr = [key for key in relayout_data.keys() if '.path' in key]
        if len(resize_arr) != 0:
            for el in resize_arr:
                new_geometry = relayout_data[el]
                idx_old = int(el[1+el.find('['):el.find(']')])
                dash.get_app().markers_class_1[idx_old]['path'] = new_geometry

        elif "shapes" in relayout_data:
            dash.get_app().state_dict['start_annotation'] = True
            dash.get_app().__setattr__('last_figure', figure)
            makrers_data = relayout_data["shapes"] 
            dash.get_app().markers_class_1 = makrers_data

    # define figure
    figure_to_return = figure
    if hasattr(dash.get_app(), 'last_figure'):
        if dash.get_app().last_figure is None:
            figure_to_return = px.imshow(dash.get_app().image.data, binary_string=True, width=800)#, height=800)
            figure_to_return.update_layout(dragmode="drawopenpath", newshape=NEWSHAPE)


    n_marked = 0
    if hasattr(dash.get_app(), 'markers_class_1'):
        n_marked = len(dash.get_app().markers_class_1)

    print('Situation unexpected x2.')
    return figure_to_return, n_marked




"""

@callback(
    Output('graph-pic', 'figure'),
    Input('button-img-show', 'n_clicks'),
    State("graph-pic", "figure"),       
    Input("slider-img-size", "value"),
    # prevent_initial_call=True
)
def show_image(n_clicks, figure, slider_value):
    print(f'SHOW IMAGE. ctx.triggered_id = {ctx.triggered_id} \n')
    # if ctx.triggered_id == 'slider-img-size' and hasattr(dash.get_app(), 'last_figure'):
    #     print(dash.get_app().last_figure.keys())
    #     fig = px.imshow(dash.get_app().image.data, binary_string=True, width=slider_value)#, height=800)
    #     fig.update_layout(dragmode="drawclosedpath")
    #     return fig
    if hasattr(dash.get_app(), 'image'):
        if dash.get_app().last_figure is not None:
            #print(dash.get_app().last_figure.keys(), dash.get_app().last_figure['data'])
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
    print(f'ON NEW ANNOTATION. ctx.triggered_id = {ctx.triggered_id} \n')
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
"""