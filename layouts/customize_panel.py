import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
from services import register_cache, earthquake_data, json_to_df, eq_count

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

def customize_panel():
   #dropdown cards to provide options for theme, time and magnitude filter
   # colour theme for the panel
   colours_graph = px.colors.named_colorscales()

   return dbc.Card([
         dbc.CardBody([
            html.H5("Customize the Earthquake Visual"),
            html.Hr(),
            html.P("Click on the tabs to switch visuals. To view earthquakes in the scatter map, zoom out on the map after selecting the theme, time window, and minimum magnitude."),
            html.Label("Theme:"),
            dcc.Dropdown(options=colours_graph, value="blackbody", id="dropdown-colour", style={'color': 'black'}),
            html.Label("Time Window:"),
            dcc.Dropdown(options=["hour", "day", "week", "month"], value="week", id="dropdown-time", style={'color': 'black'}),
            html.Br(),
            html.Label("Magnitude"),
            dcc.RangeSlider(0, 10, 1, count=1, value=[0,10], marks=None,
                     tooltip={"placement": "bottom", "always_visible": True}, 
                     id="slider-magnitude"),
            html.Label("Depth (km below)"),
            html.P("Shallow=0-70km, Intermediate=70-300km, Deep=300-700km", style={"fontSize":10}),
            dcc.RangeSlider(depth_range("month", "min"), depth_range("month", "max"), 1, count=1, value=[depth_range("month", "min"), depth_range("month", "max")], marks=None,
                     tooltip={"placement": "bottom", "always_visible": True}, 
                     id="slider-depth"),
            ]),
         ])