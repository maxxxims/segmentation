# import dash
# from dash import Dash, html, dcc, Output, Input, callback
# from flask import redirect


# dash.register_page(__name__, path = '/')


# layout = html.Div([html.Div(
#     id='start-page-text', children='Start page'),
#     dcc.Input(id='hidden-text', value = 'text', style={"display": "none"}),

#     ])


# # @callback(
# #     Output('start-page-text', 'children'),
# #     Input('hidden-text', 'value'),
# # )
# # def redirect_to_upload(value):
# #     return redirect('/upload_file')