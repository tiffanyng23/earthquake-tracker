from dash import Dash, dash_table, callback, Output, Input
from dash.dash_table.Format import Format, Scheme
from flask import Flask
from services import earthquake_data, json_to_df, eq_count
import requests
import pandas as pd

# function for table, allows for user to customize table data by time window and magnitude
def register_table_callbacks(app):
    @callback(
        Output(component_id="summary-table", component_property="data"),
        Output(component_id="summary-table", component_property="columns"),
        Input(component_id="dropdown-time", component_property="value"),
        Input(component_id="slider-magnitude", component_property="value"),
    )
    def summary_table(time, magnitude):
        #extract data for dash table
        table_data = json_to_df(earthquake_data(time))

        # filter table by selected magnitide
        filtered_table = table_data[table_data["magnitude"] >= magnitude]
        filtered_table = filtered_table[["time", "place", "magnitude"]]
        
        # dash table properties
        data = filtered_table.to_dict("records")
        columns = [
            {"name": "Time", "id": "time"},
            {"name": "Location", "id": "place"},
            {
                "name": "Magnitude", 
                "id": "magnitude", 
                "type": "numeric", 
                "format": Format(precision=2, scheme=Scheme.fixed),
            },
        ]
        return data, columns
