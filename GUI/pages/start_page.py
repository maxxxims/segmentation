import dash
from dash import Dash, html, dcc, Output, Input, callback
from flask import redirect


dash.register_page(__name__, path = '/')


layout = html.Div(id="page-content", children=[
        html.P(children=[
            html.Span("Welcome to Image Annotations Tools for Semantic Segmentation. Instructions can be found on the "),
            html.A("Tutorial", href='/tutorial'), 
            html.Span(" page or you can start from the "),
            html.A("Upload File", href='/upload_file '), html.Span(" page."),

        ], style={'text-align': 'center', 'font-size': '20pt', 'margin-bottom': '20px'}
        
        )
    ]),
