import dash
from dash import Dash, html, dcc, Output, Input, callback
from flask import redirect


dash.register_page(__name__, path = '/')

tutorial_url = 'http://162.248.227.166:8060/tutorial2'

layout = html.Div(id="page-content", children=[
        html.P(children=[
            html.Span("Welcome to Image Annotation Tools for Semantic Segmentation. Instructions can be found on the "),
            html.A("Tutorial", href=tutorial_url), 
            html.Span(" page or you can start from the "),
            html.A("Select File", href='choose_file '), html.Span(" page."),

        ], style={'text-align': 'center', 'font-size': '20pt', 'margin-bottom': '20px'}
        
        )
    ]),
