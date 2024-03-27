import base64
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update, callback, State, ctx
import dash_bootstrap_components as dbc
from skimage import data
import json
import matplotlib.pyplot as plt
import dash
import dash_daq as daq
from PIL import Image as IMG
from backend import Image
import numpy as np
from backend import draw_annotations, draw_polygons_on_last_figure, delete_polygons_on_last_figure
from GUI.utils import login_required
from GUI.database import session_table, image_table, figure_table
from flask import request
import json
import plotly.graph_objects as go


dash.register_page(__name__, path = '/annotation')


NEWSHAPE = {'opacity': 0.3, 'fillrule':'evenodd', #nonzero
             'line': {'color': 'red','dash': 'solid', "width": 4},}

WARNING_MSG_CHANGE_SELECTOR = 'Sorry, you can change this before annotating. Reload the image'


@login_required
def get_figure(img_data, username: str, height=800):
    fig = px.imshow(default_figure, binary_string=True, height=height)
    # fig.update_layout(dragmode="drawopenpath",
    #                   newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="darkblue", width=8)))
    # nonzero
    line_opacity = session_table.get_line_opacity(username)
    global NEWSHAPE
    NEWSHAPE['opacity'] = line_opacity
    fig.update_layout(dragmode="drawopenpath", 
                    newshape=NEWSHAPE)
    
    return fig


def get_options():
    return [
        {'label': 'class 1',    'value': 1},
        {'label': 'background 0', 'value': 0},
    ]


default_figure = 255 * np.ones((200, 200, 3))

# fig = get_figure(default_figure)


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

@login_required
def layout(username:  str):
    on = session_table.get_show_polygons(username)
    line_width = session_table.get_line_width(username)
    fill_opacity = session_table.get_fill_opacity(username)
    line_opacity = session_table.get_line_opacity(username)
    selected_class = session_table.get_selected_class(username=username)
    print(f'opacity = {fill_opacity}')
    layout = html.Div(
        [   
            html.Div(id='setting-container',
                                 children=[
                                    html.Span(id='btns-cnt', children=[
                                        daq.BooleanSwitch(id='show-polygons', on=on, label='Show polygons', labelPosition='top'),
                                        dbc.Button('Drop settings', id='drop-settings', color="primary", className="me-1", n_clicks=0, style={'margin-left': '10px'}),
                                    ]),
                                    
                                    html.Span(id='slider-cnt', children=[
                                         dbc.Label('Line width', html_for='widht-slider'),
                                         dcc.Slider(1, 8, value=line_width, id='widht-slider', marks=None,tooltip={"placement": "bottom", "always_visible": False} ),]),
                                    html.Span(id='slider-cnt-2', children=[
                                        dbc.Label('Fill opacity', html_for='opacity-slider'),
                                        dcc.Slider(0, 1, value=fill_opacity, id='opacity-slider', marks=None, tooltip={"placement": "bottom", "always_visible": False} ),
                                    ]),
                                    html.Span(id='slider-line-opacity', children=[
                                        dbc.Label('Line opacity', html_for='opacity-line-slider'),
                                        dcc.Slider(0, 1, value=line_opacity, id='opacity-line-slider', marks=None, tooltip={"placement": "bottom", "always_visible": False} )
                                    ])
                                     ], style={"display": "grid",
                                                "gridTemplateColumns": f"25% 25% 25% 25%",
                                                    },),
            
            html.Div(
                id='text-under-button',
                children=[
                        html.B(children="Marked segments: "),
                        html.Span(children='0', id="text-marked-segments"), html.Br(),
                        html.B(children="Selected class: "),
                        html.Span(children=selected_class, id="text-selected-class"),
                        html.Span(id='hiden-btn', hidden=True),
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
                dcc.Graph(id="graph-pic", figure=get_figure(default_figure), config=config, ),
                html.Div(
                    style={'justify-content': 'center'},
                    children=[
                        html.Button(children="Fill Background", id="button-img-fill-bg", n_clicks=0, style={ 'align': 'center'}),
                        html.Button(children="Fill Class 1", id="button-img-fill-class-1", n_clicks=0, style={ 'align': 'center'}),
                        html.H3('Annotated Image Preview', style={'text-align': 'center'}),
                    ]
                ),
                
                dcc.Graph(id="preview-annotated", figure=get_figure(default_figure), config={}),
                html.Pre(id="annotations-data-pre"),
                html.Span(id='hidden2', hidden=True),

            ]), #'justify-content': 'center', 'margin-bottom': '20px' style={'display': 'flex', }
            

            html.Div(id='container-slider-img-size', children=[
                html.P('Set image size'),
                dcc.Slider(100, 2000, marks=None, value=200, id='slider-img-size'),
            ], style={'margin-left': '5%', 'font-size': '20px', 'width': '25%'})
            
        ]
    )
    return layout


@callback(
    Output('widht-slider', 'value', allow_duplicate=True),
    Output('opacity-line-slider', 'value', allow_duplicate=True),
    Output('opacity-slider', 'value', allow_duplicate=True),
    # Output('graph-pic', 'figure', allow_duplicate=True),
    Input('drop-settings', 'n_clicks'),
    prevent_initial_call=True
)
@login_required
def drop_settings(n_clicks, username: str):
    line_width=3
    line_opacity=0.5
    fill_opacity=0.8
    session_table.update_fill_opacity(username=username, opacity=fill_opacity)
    session_table.update_line_opacity(username=username, opacity=line_opacity)
    session_table.update_line_width(username=username, line_width=line_width)
    # last_figure = figure_table.get_last_figure(username)
    # if last_figure is not None:
    #     on = session_table.get_show_polygons(username)
    #     return line_width, line_opacity, fill_opacity#, show_polygons(on)
    return line_width, line_opacity, fill_opacity#, no_update


@callback(
    Output('opacity-line-slider', 'value', allow_duplicate=True),
    Output('graph-pic', 'figure', allow_duplicate=True),
    Input('opacity-line-slider', 'value'),
    prevent_initial_call=True
)
@login_required
def change_line_opacity(value, username: str):
    session_table.update_line_opacity(username=username, opacity=value)
    global NEWSHAPE
    NEWSHAPE['opacity'] = value
    last_figure = figure_table.get_last_figure(username)
    on = session_table.get_show_polygons(username)
    print(f'line opacity = {value}')
    if last_figure is not None:
        last_figure['layout']['newshape']['opacity'] = value
        figure_table.save_last_figure(username, last_figure)
        return value, show_polygons(on)
    return value, no_update


@callback(
    Output('opacity-slider', 'value', allow_duplicate=True),
    Output('graph-pic', 'figure', allow_duplicate=True),
    Input('opacity-slider', 'value'),
    prevent_initial_call=True
)
@login_required
def change_fill_opacity(value, username: str):
    session_table.update_fill_opacity(username=username, opacity=value)
    on = session_table.get_show_polygons(username)
    return value, show_polygons(on)


@callback(
    Output('widht-slider', 'value', allow_duplicate=True),
    Output('graph-pic', 'figure', allow_duplicate=True),
    Input('widht-slider', 'value'),
    prevent_initial_call=True
)
@login_required
def change_line_width(value, username: str):
    session_table.update_line_width(username=username, line_width=value)
    print(f'line width = {value}')
    global NEWSHAPE
    NEWSHAPE['line']['width'] = value
    last_figure = figure_table.get_last_figure(username)
    on = session_table.get_show_polygons(username)
    
    if last_figure is not None:
        last_figure['layout']['newshape']['line']['width'] = value
        print(f"NEW SHape = {last_figure['layout']['newshape']['line']['width']}")
        figure_table.save_last_figure(username, last_figure)
        return value, show_polygons(on)
    return value, no_update


@callback(
    Output('graph-pic', 'figure', allow_duplicate=True),
    Input('show-polygons', 'on'),
    prevent_initial_call=True
)
@login_required
def show_polygons(on, username: str):
    last_figure = figure_table.get_last_figure(username)
    session_table.update_show_polygons(username=username, show_polygons=on)
    # print(f'on = {on}')
    if last_figure is None:
        return no_update
    img = image_table.get_image(username)
    markers_class_1 = figure_table.get_marker_class_1(username)
    if on:
        fill_opacity = session_table.get_fill_opacity(username)
        figure_to_return = draw_polygons_on_last_figure(last_figure, img, markers_class_1, reverse=__get_reverse(), alpha=fill_opacity) 
    else:
        figure_to_return = delete_polygons_on_last_figure(last_figure, img)
    return figure_to_return



@callback(
    Output('text-selected-class', 'children'),
    Output('graph-pic', 'figure', allow_duplicate=True),
    Input('dropdown-selected-class', 'value'),
    prevent_initial_call=True
)
def change_selected_class(value):
    username = request.authorization['username']
    is_started_annotation = session_table.is_start_annotation(username=username)
    # is_loaded_image = session_table.is_loaded_image(username=username)
    last_figure = figure_table.get_last_figure(username=username)
    session_table.update_selected_class(username=username, selected_class=value)
    selected_class = session_table.get_selected_class(username=username)
    if last_figure is not None:
        on = session_table.get_show_polygons(username)
        return selected_class, show_polygons(on)
    return selected_class, no_update


@callback(
    Output('preview-annotated', 'figure'),
    Input('button-img-fill-bg', 'n_clicks'),
    Input('button-img-fill-class-1', 'n_clicks'),
)
def show_preview(n_clicks1, n_clicks2):
    username = request.authorization['username']    
    marker_class_1 = figure_table.get_marker_class_1(username=username)
    is_loaded_image = session_table.is_loaded_image(username=username)

    
    if not is_loaded_image or marker_class_1 is None:
        return no_update
    
    selected_class = session_table.get_selected_class(username=username)
    reverse = False
    if ctx.triggered_id == 'button-img-fill-class-1':
        if int(selected_class) == 1:
            reverse = False
        else:
            reverse = True
    elif ctx.triggered_id == 'button-img-fill-bg':
        if int(selected_class) == 1:
            reverse = True
        else:
            reverse = False
    
    img_add, img = draw_annotations(image_table.get_image(username=username),
                                    marker_class_1, reverse=reverse)
    fig = px.imshow(img_add, binary_string=True, height=800)    
    return fig
    

@callback(
    Output('graph-pic', 'figure'),
    Output('text-marked-segments', 'children'),
    Input("graph-pic", "relayoutData"),
    State("graph-pic", "figure"),
    # prevent_initial_call=True
    
)
def on_new_annotation(relayout_data, figure, allow_duplicate=True):
    # initial call
    
    username = request.authorization['username']
    print()
    print()
    is_loaded_image = session_table.is_loaded_image(username=username)
    last_figure = figure_table.get_last_figure(username)
    if last_figure is not None:
        print(f"new shape!!!!!! = {last_figure['layout']['newshape']}")
    is_started_annotation = session_table.is_start_annotation(username=username)
    
    print(f'is_loaded_image = {is_loaded_image}; last_figure is None = {last_figure is None}') 
    if ctx.triggered_id is None:
        print(f'CTX IS NONE!')
        if not is_loaded_image:
            return get_figure(default_figure), 0
        if last_figure is not None:
            print('HERE!!!')
            return last_figure, 0
        if last_figure is None and is_loaded_image:
            img = image_table.get_image(username)
            fig = px.imshow(img, binary_string=True, height=800)
            fig.update_layout(dragmode="drawopenpath", 
                        newshape=NEWSHAPE)
            figure_table.save_marker_class_1(username, [])
            return fig, 0
        print('Situation unexpected.')
        return get_figure(default_figure), 0
    
    if relayout_data is not None and is_loaded_image:
        print('RELAYOUT DATA IS NOT NONE')
        resize_arr = [key for key in relayout_data.keys() if '.path' in key]
        if len(resize_arr) != 0:
            for el in resize_arr:
                new_geometry = relayout_data[el]
                idx_old = int(el[1+el.find('['):el.find(']')])
                markers_class_1 = figure_table.get_marker_class_1(username)
                markers_class_1[idx_old]['path'] = new_geometry
                figure_table.save_marker_class_1(username, markers_class_1)
                figure_table.save_last_figure(username, figure)
        elif "shapes" in relayout_data:
            print('SHAPES IS NOT NONE SAVE FIGURE AND CLASS 1')
            # dash.get_app().state_dict['start_annotation'] = True
            if not is_started_annotation:
                session_table.update_start_annotation(username, True)
            for el in relayout_data["shapes"]:
                if 'label' in el.keys():
                    el['label']['text'] = 'class 1'
            for shape in relayout_data["shapes"]:
                shape = {}
            figure_table.save_last_figure(username, figure)
            makrers_data = relayout_data["shapes"] 
            figure_table.save_marker_class_1(username, makrers_data)


    markers_class_1 = figure_table.get_marker_class_1(username)
    img = image_table.get_image(username)
    n_marked = 0
    if markers_class_1 is not None:
        n_marked = len(markers_class_1)
        
        
    # define figure
    last_figure = figure_table.get_last_figure(username)
    figure_to_return = figure
    if last_figure is None:
        print(f'LAST FIGURE IS NONE')
        if is_loaded_image:
            figure_to_return = px.imshow(image_table.get_image(username), binary_string=True, height=800)#, height=800)
            figure_to_return.update_layout(dragmode="drawopenpath", newshape=NEWSHAPE)
        else:
            figure_to_return = get_figure(default_figure)
        return figure_to_return, n_marked
    # count marked segments
    
    
    

    print(f'show polygon  = {session_table.get_show_polygons(username)}')
    if session_table.get_show_polygons(username) and last_figure is not None:
        fill_opacity = session_table.get_fill_opacity(username)
        figure_to_return = draw_polygons_on_last_figure(figure_to_return, img, markers_class_1, reverse=__get_reverse(), alpha=fill_opacity) 
    return figure_to_return, n_marked



@login_required
def __get_reverse(username: str):
    return False
    selected_class = session_table.get_selected_class(username)
    if selected_class == 1:
        return False
    else:
        return True