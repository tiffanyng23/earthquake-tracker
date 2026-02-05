import dash_bootstrap_components as dbc
from dash import html, dcc
from services import register_cache, earthquake_data, json_to_df, eq_count

#CARDS 
#Summary dashboard showing total earthquakes over the past hour, day, week, month
#create 4 cards for total earthquake count (month, week, day, hour)

#find min and max earthquake depth for time window for a month to set range
def depth_range(time_window, min_or_max):
    #api
    depth_json = earthquake_data(time_window)
    # get depth column data
    depth_df = json_to_df(depth_json)[["depth"]]
    if min_or_max == "min":
        return int(depth_df.min().item())
    if min_or_max == "max":
        return int(depth_df.max().item())


def summary_dashboard():
    return dbc.CardGroup([
        #select magnitude for total count dropdown card
        dbc.Card([
            dbc.CardBody([
                html.H5("Magnitude", className="text-center"),
                dcc.RangeSlider(0, 10, 1, count=1, value=[0,10], marks=None,
                    tooltip={"placement": "bottom", "always_visible": True}, 
                    id="summary-magnitude"),
            ])
        ]),
        dbc.Card([
            dbc.CardBody([
                html.H5("Depth (km below)", className="text-center"),
                dcc.RangeSlider(depth_range("month", "min"), depth_range("month", "max"), 1, count=1, value=[depth_range("month", "min"), depth_range("month", "max")], marks=None,
                    tooltip={"placement": "bottom", "always_visible": True}, 
                    id="summary-depth"),
            html.P("Shallow=0-70km, Intermediate=70-300km, Deep=300-700km", style={"fontSize":10}),
            ]),
        ]),
        dbc.Card([
            dbc.CardBody([
                html.H5("Past 30 Days:", className="text-center"),
                html.H3(id="count-month", className="text-center")
            ])
        ]),
        dbc.Card([
            dbc.CardBody([
                html.H5("Past 7 Days:", className="text-center"),
                html.H3(id="count-week", className="text-center")
            ])
        ]),
        dbc.Card([
            dbc.CardBody([
                html.H5("Past Day:", className="text-center"),
                html.H3(id="count-day", className="text-center")
            ])
        ]),
        dbc.Card([
            dbc.CardBody([
                html.H5("Past Hour:", className="text-center"),
                html.H3(id = "count-hour", className="text-center")
            ])
        ]), 
    ])
