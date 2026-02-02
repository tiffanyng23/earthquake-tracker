import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px

def customize_panel():
   #dropdown cards to provide options for theme, time and magnitude filter
   # colour theme for the panel
   colours_graph = px.colors.named_colorscales()

   return dbc.Card([
         dbc.CardBody([
            html.H5("Customize the Earthquake Visual"),
            html.Hr(),
            html.P("To view earthquakes, zoom out on the map after selecting time window and minimum magnitude."),
            html.Label("Theme:"),
            dcc.Dropdown(options=colours_graph, value="agsunset", id="dropdown-colour", style={'color': 'black'}),
            html.Label("Time Window:"),
            dcc.Dropdown(options=["hour", "day", "week", "month"], value="month", id="dropdown-time", style={'color': 'black'}),
            html.Br(),
            html.Label("Minimum Magnitude:"),
            dcc.Slider(0, 10, 1, value=4, marks=None,
                     tooltip={"placement": "bottom", "always_visible": True}, 
                     id="slider-magnitude"),
         ])
      ])