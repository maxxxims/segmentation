import dash
from dash import Dash, html, dcc, Output, Input
from .callbacks import on_new_annotation
from .program.programm import Programm
from flask import redirect
from flask import Flask


server = Flask(__name__)
app = Dash(__name__, use_pages=True, server=server)


button_styles = {'margin-left': '40px', 'width': '10%', 'height': 'auto'}

app.layout = html.Div([
    html.H1('Image annotations tools for semantic segmentation', style={'textAlign': 'center'}),
    html.Div(id='navigate-bar', children=[
        html.Button(style=button_styles, children=[html.A("Tutorial", href='/')]),
        html.Button(style=button_styles, children=[html.A("Upload File", href='/upload_file')]),
        html.Button(style=button_styles, children=[html.A("Annotation", href='/annotation')]),
        html.Button(style=button_styles, children=[html.A("Save file", href='/annotation_background')]),
        # html.Button(style={'align': 'center'}, children=[html.A("Annotation", href='/')]),

    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '20px'}),

    # html.Div([
    #     html.Div(
    #         dcc.Link(f"{page['name']}{page['path']}", href=page["relative_path"])
    #     ) for page in dash.page_registry.values()
    # ]),
    dash.page_container
], style={'margin-bottom': '100px'})

# from .pages.annotation import img


# @app.callback(
#     Output("annotations-data-pre", "children"),
#     Input("graph-pic", "relayoutData"),
#     prevent_initial_call=True,
# )
# def on_new_annotation_callback(relayout_data):
#     on_new_annotation(relayout_data)  

@server.route('/test')
def test():
    return {'msg': 'test'}

@server.route('/ale/upload_file')
def upload_file():
    return {'msg': 'tester'}

# @app.server.route('/')
# def redirect():
#     return redirect('/upload_file')




if __name__ == '__main__':
    
    # img.load_image()
    
    app.run(debug=True)