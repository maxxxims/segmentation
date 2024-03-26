from dash import Dash, dcc, html, Input, Output, State, callback, no_update, dash_table
import plotly.express as px
import dash
from backend import Image, parse_json_file
import io
import json
from PIL import Image as IMG
import base64
import numpy as np
from matplotlib import pyplot as plt
from GUI.database import session_table, image_table, figure_table, task_table, user2task_table
from GUI.utils import login_required
from flask import request


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash.register_page(__name__, path = '/choose_file')

next_step_button = {
    'align': 'center',
}


@login_required
def get_available_tasks(username: str):
    print(f'username = {username}')
    options = []
    tasks = user2task_table.get_available_tasks(username)
    for t in tasks:
        options.append({
            'label': f'{t.image_name}; attempt {t.attempt_number}',
            'value': t.task_id,
        })
    return options


@login_required
def get_info_table(username: str):
    user_tasks = user2task_table.get_all_tasks(username)
    tasks = []
    cols = ['Image name', 'Attempt number', 'Is finished', 'Accuracy']
    for t in user_tasks:
        print(tasks)
        tasks.append({'image_name': t.image_name, 'attempt_number': t.attempt_number,
                      'finished': t.finished, 'accuracy': t.metric})
        
    layout = dash_table.DataTable(tasks, columns=[{'name': col, 'id': col} for col in cols])
                                 # cell_selectable=False, style_header={'textAlign': 'center', 'font-weight': 'bold'})
    return layout


def layout():
    layout = html.Div([
        html.Div(id='output-image-upload-default2'),
        html.Div(id='dropdown-menu2',
                 children=[
                    dcc.Dropdown(id='select-task', options=get_available_tasks(),
                                 style={'margin-left': 'auto', 'margin-right': 'auto' },
                                 placeholder='Select task'),
                    html.Div(id='uploaded-img')
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
    Output('uploaded-img', 'children'),
    Input('select-task', 'value'),
)
@login_required
def choose_task(task_id, username: str):
    print(f'task_id = {task_id}')
    #import os
    #print(f'dir = {os.listdir()}')
    if task_id is not None:
        task = task_table.get_task_by_id(task_id)
        with open(task.path_to_json, 'r') as file:
            json_data = json.load(file)
        img = np.load(task.path_to_image)
        
        image_table.save_image(username, img)
        figure_table.save_json_data(username=username, json_data=json_data)
        session_table.update_loaded_image(username=username, loaded_image=True)
    
    
    if session_table.is_loaded_image(username):
        json_data = figure_table.get_json_data(username=username)
        file_name = json_data['image_tag'] + '.json'
        return show_image(username, file_name)
    else:
        return html.Div(children=[html.H3('Image is not loaded yet', style={'text-align': 'center'})])