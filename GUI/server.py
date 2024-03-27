from pathlib import Path
import dash
from dash import Dash, html, dcc, Output, Input
from flask import redirect, Flask, render_template
from .database.db import init_db, drop_db, drop_redis
from .database import user_table, session_table, task_table, user2task_table
from .utils import get_users, add_tasks_to_users, register_user, make_tasks_from_folder
import dash_auth
from .config import Config


server = Flask(__name__)
app = Dash(__name__, use_pages=True, server=server, url_base_pathname='/')


button_styles = {'margin-left': '40px', 'width': '10%', 'height': 'auto'}

app.layout = html.Div([
    html.H1('Image annotations tools for semantic segmentation', style={'textAlign': 'center'}),
    html.Div(id='navigate-bar', children=[
        html.Button(style=button_styles, children=[html.A("Tutorial", href='/tutorial')]),
        html.Button(style=button_styles, children=[html.A("Choose File", href='/choose_file')]),
        html.Button(style=button_styles, children=[html.A("Annotation", href='/annotation')]),
        html.Button(style=button_styles, children=[html.A("Save file", href='/annotation_background')]),


    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '20px'}),
    dash.page_container
], style={'margin-bottom': '100px'})



@server.route('/tutorial')
def test():
    return render_template('tutorial0.html')



if __name__ == '__main__':
    print('Application is available at http://127.0.0.1:8050/')
    # from GUI.database.db import engine
    # from GUI.database.models import User2Task, Task
    # from sqlalchemy import select, update
    # from uuid import UUID
    # with engine.begin() as conn:
    #     # result = conn.execute(select(User2Task, Task).join(Task, Task.id == User2Task.task_id).having(User2Task.uuid == uuid)).all()
    #     conn.execute(update(User2Task).where(User2Task.uuid == UUID('5d5ae7c9-beee-4ffe-8d2f-bba2a7c33c23')).values(is_choosen=False))
    #     result = conn.execute(select(User2Task, Task).join(Task, Task.id == User2Task.task_id).where(User2Task.uuid == UUID('5d5ae7c9-beee-4ffe-8d2f-bba2a7c33c23'))).all()
        
    # for el in result:
    #     print(el)
    
    
    drop_redis()
    
    drop_db()
    init_db()
    # user_table.add_user(username='admin', password='admin')
    # user_table.add_user(username='admin2', password='admin2')
    
    # session_table.create_session(username='admin')
    # session_table.create_session(username='admin2')
    
    # task_table.add_task(image_name='ex0_300', path_to_json='data/ex0_300.json',
    #                     path_to_image='data/input/ex0_300.npy', path_to_annotated_image='data/input/ex0_300_annotated.npy')
    # task_table.add_task(image_name='ex1_300', path_to_json='data/ex1_300.json',
    #                     path_to_image='data/input/ex1_300.npy', path_to_annotated_image='data/input/ex1_300_annotated.npy')
    # task_table.add_task(image_name='ex2_300', path_to_json='data/ex2_300.json',
    #                     path_to_image='data/input/ex2_300.npy', path_to_annotated_image='data/input/ex2_300_annotated.npy')
    # task_table.add_task(image_name='ex3_300', path_to_json='data/ex3_300.json',
    #                     path_to_image='data/input/ex3_300.npy', path_to_annotated_image='data/input/ex3_300_annotated.npy')
    
    
    # user2task_table.add_task(username='admin', task_id=1)
    # user2task_table.add_task(username='admin', task_id=3)
    
    # user2task_table.add_task(username='admin2', task_id=1)
    
    register_user(username='admin', passwrod='admin')
    register_user(username='user1', passwrod='123')
    make_tasks_from_folder(path_to_folder=Path('data'), path_to_input_folder=Path('data/input'))
    add_tasks_to_users(attempts_per_user=3)
    
    auth = dash_auth.BasicAuth(
                                app,
                                get_users() 
                                )
    HOST = Config.get_gui_host()
    PORT = Config.get_gui_port()
    app.run(host=HOST, port=PORT, debug=True)
    
    """
    2) Сделать новые образцы для разметки 4-5 штук
    3) Развертка на сервере, добавление пользователей +-
    4) Дизайн   
    6) просмотр полноразмерного изображения
    """
    
    