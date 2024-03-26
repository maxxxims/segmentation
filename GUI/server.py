import dash
from dash import Dash, html, dcc, Output, Input
from .callbacks import on_new_annotation
from flask import redirect, Flask, render_template
from .database.db import init_db, drop_db, drop_redis
from .database import user_table, session_table, task_table, user2task_table
from .utils import get_users
import dash_auth


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
    # from sqlalchemy import select
    # with engine.connect() as conn:
    #     res = conn.execute(select(User2Task, Task).join(Task, Task.id == User2Task.task_id)).all()
    #     # print(res)
    # for el in res:
    #     print(el.username, el.image_name)
    # print(res[0].user_tasks)
    drop_redis()
    
    drop_db()
    init_db()
    user_table.add_user(username='admin', password='admin')
    session_table.create_session(username='admin')
    task_table.add_task(image_name='ex0_300', path_to_json='data/ex0_300.json',
                        path_to_image='data/input/ex0_300.npy', path_to_annotated_image='data/input/ex0_300_annotated.npy')
    task_table.add_task(image_name='ex1_300', path_to_json='data/ex1_300.json',
                        path_to_image='data/input/ex1_300.npy', path_to_annotated_image='data/input/ex1_300_annotated.npy')
    task_table.add_task(image_name='ex2_300', path_to_json='data/ex2_300.json',
                        path_to_image='data/input/ex2_300.npy', path_to_annotated_image='data/input/ex2_300_annotated.npy')
    task_table.add_task(image_name='ex3_300', path_to_json='data/ex3_300.json',
                        path_to_image='data/input/ex3_300.npy', path_to_annotated_image='data/input/ex3_300_annotated.npy')
    
    
    user2task_table.add_task(username='admin', task_id=1)
    user2task_table.add_task(username='admin', task_id=3)
    
    
    auth = dash_auth.BasicAuth(
                                app,
                                get_users() 
                                )
    app.run(host='0.0.0.0', port=8050, debug=True)
    
    