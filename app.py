from callbacks import register_callbacks
from dash import Dash, dash_table, html, dcc, callback, Output, Input
from dash.dash_table.Format import Format, Scheme
from flask import Flask
from flask_caching import Cache
from layouts.tabs import tabs_layout
from layouts.summary_cards import summary_dashboard
from layouts.customize_panel import customize_panel
from services import earthquake_data, json_to_df, eq_count
import requests
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

#CREATE APP
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server

#APP LAYOUT
app.layout = dbc.Container([
    # title of dashboard
    dbc.Row([
        html.H1(children='Global Earthquake Tracker', className="text-center"),
    ]),

    #displays earthquake counter
    dbc.Row([
        html.Hr(),
        summary_dashboard(),
        html.Hr(),
    ], justify="center"),

    #displays customization panel and 3 tabs with visualizations
    dbc.Row([
        dbc.Col(customize_panel(), md=3),
        dbc.Col(tabs_layout(), md=9)
    ], align="center", justify="center")
], fluid=True)

#callbacks which gathers inputs from app.layout
#output displayed on app.layout
register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
