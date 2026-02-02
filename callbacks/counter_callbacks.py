from dash import Dash, callback, Output, Input
from flask import Flask
import pandas as pd
import requests
from services import earthquake_data, json_to_df, eq_count

#Summary dashboard
def register_counter_callbacks(app):
    @callback(
        Output(component_id= "count-hour", component_property="children"),
        Output(component_id= "count-day", component_property="children"),
        Output(component_id= "count-week", component_property="children"),
        Output(component_id= "count-month", component_property="children"),
        Input(component_id="summary-magnitude", component_property="value")
    )
    # count earthquakes, filter by magnitude and stratify by time
    def summary_tracker(magnitude):
        magnitude = float(magnitude) 
        # store earthquake counts by time window in dictionary
        # time : earthquake count
        eq_totals = {"hour":0, "day":0, "week":0, "month":0}

        for time in eq_totals.keys():
            #collect earthquake data for specified time thresholds (hour, day, month, week)
            raw_features = earthquake_data(time)
            raw_features = json_to_df(raw_features)

            # count earthquakes that fit requested magnitude, update dictionary values
            # filter for rows where magnitude meets threshold
            eq_totals[time] = len(raw_features[raw_features["magnitude"] >= magnitude])

        # return each of the values
        return eq_totals["hour"], eq_totals["day"], eq_totals["week"], eq_totals["month"]