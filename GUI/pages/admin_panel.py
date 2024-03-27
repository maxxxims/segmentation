from uuid import UUID
from dash import Dash, dcc, html, Input, Output, State, callback, no_update, dash_table
import plotly.express as px
import dash
from matplotlib import pyplot as plt
from GUI.database import session_table, image_table, figure_table, task_table, user2task_table
from GUI.utils import login_required, update_current_task
from flask import request
import dash_bootstrap_components as dbc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash.register_page(__name__, path = '/admin_panel')

next_step_button = {
    'align': 'center',
}



def get_info_table():
    users_info = user2task_table.get_users_tasks_info()
    cols = ['Username', 'name', 'finished', 'last activity']
    rows = []
    for t in users_info:
        finished = f'{t.sum_1} / {t.count_1}'
        rows.append({
            'Username': t.username, 'name': t.name,
            'finished': finished, 'last activity': t.last_activity.strftime(f"%H:%M %d-%m-%Y ")
        })
    
    table = html.Div([  
        dash_table.DataTable(rows, id='users-table-for-admin', columns=[{'name': col, 'id': col} for col in cols],
                                 cell_selectable=True, style_header={'textAlign': 'center', 'font-weight': 'bold'})
    ])
    return table


@login_required
def layout(username):
    if username != 'admin':
        return html.Div('Page not found', id='page-not-found-')
    # layout = get_info_table()
    return get_info_table()