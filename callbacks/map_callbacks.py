from dash import Dash, callback, Output, Input
from flask import Flask
from flask_caching import Cache
from services import earthquake_data, json_to_df, eq_count
from layouts.customize_panel import customize_panel
import requests
import pandas as pd
import plotly.express as px

#visualizations
#earthquakes visual based on theme, time, and magnitude
def register_map_callbacks(app):
    @callback(
        Output(component_id="scatter-map", component_property="figure"),
        Input(component_id="dropdown-colour", component_property="value"),
        Input(component_id="dropdown-time", component_property="value"),
        Input(component_id="slider-magnitude", component_property="value"),
    )
    def earthquake_figure(colour, time, magnitude):
        #api request - pull earthquakes for specified time window
        raw_features = earthquake_data(time)
        raw_features = json_to_df(raw_features)
        
        #filter earthquakes in selected time window that fit magnitude threshold
        filtered_features = raw_features[raw_features["magnitude"] >= magnitude]

        # display map with earthquakes
        fig = px.scatter_map(
            # plotly loops through filtered df row by row and plots earthquake
            filtered_features,
            lon= "longitude",
            lat= "latitude",
            size = "magnitude",
            color= "magnitude",
            hover_name = "place",
            hover_data = ["time", "magnitude", "longitude", "latitude"],
            color_continuous_scale = colour)
        
        fig.update_layout(
            map_style="open-street-map",
            font_color="rgba(255, 255, 255, 0.75)",
            paper_bgcolor="rgba(0,0,0,0)", 
            dragmode="zoom",
        )
        return fig