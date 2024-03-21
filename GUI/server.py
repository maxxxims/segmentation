import dash
from dash import Dash, html, dcc, Output, Input
from .callbacks import on_new_annotation
from flask import redirect, Flask, render_template
from .database.db import init_db, drop_db
from .database import user_table, session_table
from .utils import get_users
import dash_auth


server = Flask(__name__)
app = Dash(__name__, use_pages=True, server=server, url_base_pathname='/')


button_styles = {'margin-left': '40px', 'width': '10%', 'height': 'auto'}

app.layout = html.Div([
    html.H1('Image annotations tools for semantic segmentation', style={'textAlign': 'center'}),
    html.Div(id='navigate-bar', children=[
        html.Button(style=button_styles, children=[html.A("Tutorial", href='/tutorial')]),
        html.Button(style=button_styles, children=[html.A("Upload File", href='/upload_file')]),
        html.Button(style=button_styles, children=[html.A("Annotation", href='/annotation')]),
        html.Button(style=button_styles, children=[html.A("Save file", href='/annotation_background')]),


    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '20px'}),
    dash.page_container
], style={'margin-bottom': '100px'})



@server.route('/tutorial')
def test():
    return render_template('tutorial0.html')



if __name__ == '__main__':
    app.__setattr__('state_dict', {'selected_class':
                                    '1'})
    print('Application is available at http://127.0.0.1:8050/')
    drop_db()
    #init_db()
    #user_table.add_user(username='admin', password='admin')
    #session_table.create_session(username='admin')

    auth = dash_auth.BasicAuth(
                                app,
                                get_users() 
                                )
    app.run(host='0.0.0.0', port=8050, debug=True)