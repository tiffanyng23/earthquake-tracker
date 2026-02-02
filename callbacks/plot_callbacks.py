from dash import Dash, callback, Output, Input
from flask import Flask
from flask_caching import Cache
from services import earthquake_data, json_to_df, eq_count
from layouts.tabs import tabs_layout
from layouts.summary_cards import summary_dashboard
from layouts.customize_panel import customize_panel
import requests
import pandas as pd
import plotly.express as px

def register_plot_callbacks(app):
    @callback(
        Output(component_id="scatter-plot", component_property="figure"),
        Input(component_id="dropdown-colour", component_property="value"),
        Input(component_id="dropdown-time", component_property="value"),
        Input(component_id="slider-magnitude", component_property="value"),
    )
    def scatterplot(colour, time, magnitude):
        # pull earthquake data
        raw_features = earthquake_data(time)
        raw_features = json_to_df(raw_features)

        #filter data frame by magnitude
        filtered_features = raw_features[raw_features["magnitude"] >= magnitude]

        # display map with earthquakes
        fig = px.scatter(
            filtered_features,
            x= "time",
            y= "magnitude",
            size = "magnitude",
            color= "magnitude",
            hover_name = "place",
            color_continuous_scale = colour,)
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color= "rgba(255, 255, 255, 0.75)",
        )
        return fig