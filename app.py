from callbacks import register_callbacks
from dash import Dash, dash_table, html, dcc, callback, Output, Input
from dash.dash_table.Format import Format, Scheme
from flask import Flask
from flask_caching import Cache
from layouts.tabs import tabs_layout
from layouts.summary_cards import depth_range, summary_dashboard
from layouts.customize_panel import depth_range, customize_panel
from services import register_cache, earthquake_data, json_to_df, eq_count
import requests
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

#CREATE APP
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server

#cache - 300s timeout
cache = Cache(server, config = {
    "DEBUG": True,          
    "CACHE_TYPE": "SimpleCache", 
    "CACHE_DEFAULT_TIMEOUT": 300
})

register_cache(cache)

#APP LAYOUT
app.layout = dbc.Container([
    # title of dashboard
    dbc.Row([
        html.H1(children="Global Earthquake Tracker", className="text-center"),
        html.A(children="Data sourced from the USGS", 
            href="https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php", 
            target="_blank",
            className="text-center",
            style= {"color": "rgba(116,155,194,1)"}
        )
    ]),

    #displays earthquake counter
    dbc.Row([
        html.Hr(),
        summary_dashboard(),
        html.Hr(),
    ], align="center", justify="center"),

    #displays customization panel and 3 tabs with visualizations
    dbc.Row([
        dbc.Col(customize_panel(), md=3, className="mt-1"),
        dbc.Col(tabs_layout(), md=9)
    ], align="start", justify="center")
], fluid=True)

#callbacks which gathers inputs from app.layout
#output displayed on app.layout
register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
