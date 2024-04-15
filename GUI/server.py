from pathlib import Path
import dash
from dash import Dash, html, dcc, Output, Input
from flask import redirect, Flask, render_template
from .database.db import init_db, drop_db, drop_redis
from .utils import get_users, add_tasks_to_users, register_user, make_tasks_from_folder,\
    register_users_from_csv, register_admin, start_sessions, register_local_user
import dash_auth
from .config import Config
import dash_bootstrap_components as dbc
import logging


logging.basicConfig(level=logging.INFO)

server = Flask(__name__)
app = Dash(__name__, use_pages=True, server=server, url_base_pathname='/v2/',
           external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.css.append_css(
    {'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.1/css/all.min.css'}
)

button_styles = {'margin-left': '40px', 'width': '10%', 'height': 'auto'}
BTN_COLOR = 'info'
outline = True
NAVBAR_COLOR='light'

navbar = dbc.Navbar(
    html.H1('Image annotation tools for semantic segmentation', style={'textAlign': 'center'},
    ),
    color=NAVBAR_COLOR,
    dark=True, style={'text-align': 'center', 'justify-content': 'center'}, 
)

app.layout = html.Div([
    navbar,
    dbc.Navbar(id='navigate-bar', children=[
        dbc.Button(style=button_styles, color=BTN_COLOR, children='Tutorial', href=Config.get_tutorial_url(), outline=outline),
        dbc.Button(style=button_styles, color=BTN_COLOR, children='Select File', href='choose_file', outline=outline),
        dbc.Button(style=button_styles, color=BTN_COLOR, children='Annotation', href='annotation', outline=outline),
        dbc.Button(style=button_styles, color=BTN_COLOR, children='Save file', href='annotation_background', outline=outline),

    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '5px'}, color=NAVBAR_COLOR),
    dash.page_container
], style={'margin-bottom': '100px'})


if __name__ == '__main__':
    server.secret_key = 'super secret key'
    # drop_redis()
    # drop_db() 
    # init_db()

    # register_local_user(username='local', password='123')
    # register_admin()
    # register_users_from_csv('users.csv')
    # start_sessions()
    # make_tasks_from_folder(path_to_folder=Path('data'), path_to_input_folder=Path('data/input'))
    # add_tasks_to_users(attempts_per_user=3)
    
    
    auth = dash_auth.BasicAuth(
                                app,
                                get_users() 
                                )
    HOST = Config.get_gui_host()
    PORT = Config.get_gui_port()
    print(f'Application is available at http://127.0.0.1:{PORT}/')
    app.run(host=HOST, port=PORT, debug=True)