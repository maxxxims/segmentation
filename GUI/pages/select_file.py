from uuid import UUID
from dash import Dash, dcc, html, Input, Output, State, callback, no_update, dash_table, ctx
import dash
from backend import Image, parse_json_file
import io
import json
from PIL import Image as IMG
import numpy as np
from matplotlib import pyplot as plt
from GUI.database import session_table, image_table, figure_table, task_table, user2task_table
from GUI.utils import login_required, update_current_task
import dash_bootstrap_components as dbc


dash.register_page(__name__, path = '/choose_file')


@login_required
def get_available_tasks(username: str):
    print(f'username = {username}')
    options = []
    tasks = user2task_table.get_available_tasks(username)
    for t in tasks:
        options.append({
            'label': f'{t.image_name}; attempt {t.attempt_number}',
            'value': str(t.uuid),
        })
    return options


def __get_conditions(tasks: list):
    WHITE = 'rgb(255, 255, 255)'
    GRAY = 'rgb(240, 240, 240)'
    colors_arr = []
    previous_name = tasks[0]['Image name']
    current_color = GRAY
    for el in tasks:
        if el['Image name'] != previous_name:
             if current_color == WHITE:   current_color = GRAY
             else:  current_color = WHITE
        colors_arr.append(current_color)
        previous_name = el['Image name']
        
    return [{'if': {'row_index': i}, 'backgroundColor': colors_arr[i]} for i in range(len(tasks))]
    

@login_required
def get_info_table(username: str):
    user_tasks = user2task_table.get_all_tasks(username)
    tasks = []
    cols = ['Image name', 'Attempt number', 'Is finished', 'Accuracy', ' ']
    finished_task_number = 0
    for t in user_tasks:
        metric = round(t.metric, 2) if t.metric is not None else '-'
        finished = '✅' if t.finished else '❌'
        if t.finished:
            finished_task_number += 1
        tasks.append({'Image name': t.image_name, 'Attempt number': t.attempt_number,
                      'Is finished': finished, 'Accuracy': metric, ' ': 'click to choose'})
    
    table = html.Div([
        html.Span(children=[
            html.B(f'Finished: '), html.Span(f'{finished_task_number} / {len(user_tasks)}'), html.Br(),
        ]),
        
        html.Span('Click on the last column to choose a task (including finished ones to remake)'),
        dash_table.DataTable(tasks, id='tasks-table', columns=[{'name': col, 'id': col} for col in cols],
                                 cell_selectable=True, style_header={'textAlign': 'center', 'font-weight': 'bold'},
                                style_data_conditional=__get_conditions(tasks))
    ])
    return table

@login_required
def layout(username: str):
    current_task_uuid = user2task_table.get_current_task_uuid(username=username)
    if current_task_uuid is not None:   current_task_uuid = str(current_task_uuid)
    layout = html.Div([
        html.Div(id='output-image-upload-default2'),
        html.Div(id='dropdown-menu2',
                 children=[
                    dcc.Dropdown(id='select-task', options=get_available_tasks(), value=current_task_uuid,
                                 style={'margin-left': 'auto', 'margin-right': 'auto' },
                                 placeholder='Select task'),
                    html.Center(id='uploaded-img')
                     ], style={'width': '30%', 'margin-left': 'auto', 'margin-right': 'auto'}),
        html.Div(id='main-cnt', children=[        
        html.Div(id='output-image-upload'),
        html.Div(id='info-table', children=[
            html.H3(id='Info table', children='Tasks information', style={'text-align': 'center'}),
            get_info_table()], style={'margin-left': '20%', 'margin-right': '20%'}),
        ], style = {
                'alignContnent': 'center',
                'align': 'center',
                'postion': 'absolute',
    })
        
    ])
    return layout


def show_image(username: str, file_name: str):
    image_data = image_table.get_image(username)
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


@callback(
    Output('uploaded-img', 'children', allow_duplicate=True),
    Input('select-task', 'value'),
    prevent_initial_call='initial_duplicate'
    # prevent_initial_call=True
)
@login_required
def choose_task(task_uuid: str, username: str):
    if task_uuid is not None and ctx.triggered_id is not None:
        task_uuid = UUID(task_uuid)
        new_task = user2task_table.get_task_by_uuid(task_uuid) #task_table.get_task_by_id(task_id)
        with open(new_task.path_to_json, 'r') as file:
            json_data = json.load(file)
        _img = np.load(new_task.path_to_image)
        img = np.zeros((*_img.shape, 3), dtype=np.uint8)
        for i in range(3):
            img[:, :, i] = _img
        update_current_task(username=username, task_uuid=task_uuid, img=img, json_data=json_data)
    
    if session_table.is_loaded_image(username):
        json_data = figure_table.get_json_data(username=username)
        atempt_number = user2task_table.get_current_task_attempt_number(username=username)
        file_name = json_data['image_tag'] + f' attempt {atempt_number}'#'.json'
        return show_image(username, file_name)
    else:
        return html.Div(children=[html.H3('Image is not loaded yet', style={'text-align': 'center'})])
    
    
    
@callback(Output('uploaded-img', 'children', allow_duplicate=True),
          Input('tasks-table', 'active_cell'),
          prevent_initial_call=True)
@login_required
def select_task_from_table(active_cell, username):
    if active_cell['column_id'] == ' ':
        user_tasks = user2task_table.get_all_tasks(username)
        task_uuid = str(user_tasks[active_cell['row']].uuid)
        current_task_uuid = str(user2task_table.get_current_task_uuid(username=username))
        if current_task_uuid == task_uuid:
            return no_update
        return choose_task(task_uuid)
    else:
        return no_update