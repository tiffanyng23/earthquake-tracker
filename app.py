from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import numpy as np 
import requests
import plotly.express as px
import dash_bootstrap_components as dbc
import os


#GET EARTHQUAKE DATA FROM API'S
#function to extract places, magnitudes, longitudes, latitudes and add onto lists
def extract_spec_features(mag_limit, features=[], places=[], magnitudes=[], longitudes=[], latitudes=[]):
    """extract info about earthquake, filters earthquakes by magnitude"""
    try:
        for eq in features:
            mag = eq["properties"]["mag"] 
            #find the magnitude of the earthquake, check if it meets magnitude condition
            if mag >= mag_limit:
                place = eq["properties"]["place"]
                long = eq["geometry"]["coordinates"][0]
                lat = eq["geometry"]["coordinates"][1]
                places.append(place)
                magnitudes.append(mag)
                longitudes.append(long)
                latitudes.append(lat)
            else:
                continue
    except TypeError:
        print("Mag_limit must be an integer or float!")
    finally:
        return places, magnitudes, longitudes, latitudes

#DATA - PAST 30 DAYS:
#all earthquakes worldwide in the past 30 days with a magnitude >= 1.0
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_month.geojson"
#sending api request
response = requests.get(url)
#converting to a dictionary
response = response.json()
#extract specified features
eq_features = response["features"]

#getting data for eathquakes with a magnitude > 1
places, magnitudes, longitudes, latitudes = [],[],[],[]
month_eq = extract_spec_features(0.5, eq_features, places, magnitudes, longitudes, latitudes)
#getting data for eathquakes with a magnitude > 4.0
places_4, magnitudes_4, longitudes_4, latitudes_4 = [],[],[],[]
month_eq_4 = extract_spec_features(4, eq_features, places_4, magnitudes_4, longitudes_4, latitudes_4)
#getting data for eathquakes with a magnitude > 5.5
places_5, magnitudes_5, longitudes_5, latitudes_5 = [],[],[],[]
month_eq_5 = extract_spec_features(5.5, eq_features, places_5, magnitudes_5, longitudes_5, latitudes_5)

#PAST 7 DAYS
#earthquakes in the past 7 days with a magnitude >= 1.0
url_week = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.geojson"
response_week = requests.get(url_week)
response_week = response_week.json()
#magnitude 1 and higher
eq_week_features = response_week["features"]
places_week, mag_week, long_week, lat_week = [], [], [], []
week_eq = extract_spec_features(0.5, eq_week_features, places_week, mag_week, long_week, lat_week)
#magnitude 4.0 and higher
places_week_4, mag_week_4, long_week_4, lat_week_4 = [], [], [], []
week_eq_4 = extract_spec_features(4, eq_week_features, places_week_4, mag_week_4, long_week_4, lat_week_4)
#magnitude 5.5 and higher
places_week_5, mag_week_5, long_week_5, lat_week_5 = [], [], [], []
week_eq_5 = extract_spec_features(5.5, eq_week_features, places_week_5, mag_week_5, long_week_5, lat_week_5)


#PAST DAY
#earthquakes for the past day with a magnitude >= 1.0
url_day = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_day.geojson"
response_day = requests.get(url_day)
response_day = response_day.json()
#magnitude 1 and higher:
eq_day_features = response_day["features"]
places_day, mag_day, long_day, lat_day = [], [], [], []
day_eq = extract_spec_features(0.5, eq_day_features, places_day, mag_day, long_day, lat_day)
#4.0 and higher
places_day_4, mag_day_4, long_day_4, lat_day_4 = [], [], [], []
day_eq_4 = extract_spec_features(4, eq_day_features, places_day_4, mag_day_4, long_day_4, lat_day_4)
#5.5 and higher
places_day_5, mag_day_5, long_day_5, lat_day_5 = [], [], [], []
day_eq_5 = extract_spec_features(5.5, eq_day_features, places_day_5, mag_day_5, long_day_5, lat_day_5)


#PAST HOUR
#earthquakes for the past hour with a magnitude >= 1.0
url_hour = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_hour.geojson"
response_hour = requests.get(url_hour)
response_hour = response_hour.json()
#earthquakes with magnitude 1 and higher:
eq_hour_features = response_hour["features"]
places_hour, mag_hour, long_hour, lat_hour = [], [], [], []
eq_hour = extract_spec_features(0.5,eq_hour_features, places_hour, mag_hour, long_hour, lat_hour)
#getting data for eathquakes with a magnitude > 4.0
places_hour_4, mag_hour_4, long_hour_4, lat_hour_4 = [], [], [], []
eq_hour_4 = extract_spec_features(4, eq_hour_features, places_hour_4, mag_hour_4, long_hour_4, lat_hour_4)
#getting data for eathquakes with a magnitude > 5.5
places_hour_5, mag_hour_5, long_hour_5, lat_hour_5 = [], [], [], []
eq_hour_5 = extract_spec_features(5.5,eq_hour_features, places_hour_5, mag_hour_5, long_hour_5, lat_hour_5)

#FUNCTION TO GET TOTAL EATHQUAKES BASED ON MAGNITUDE: 
def eq_count(magnitude_limit, features=[]):
    eq_count=[]
    for eq in features:
        if eq["properties"]["mag"] >= magnitude_limit:
            eq_count.append(eq)
    return eq_count


#COLOURS FOR VISUALIZATIONS
#colour scales for graphs
colours_graph = px.colors.named_colorscales()


#CARDS 
#dashboard showing current total earthquakes over the past hour, day, week, month
#create 4 cards for total count - to be displayed underneath the title
dashboard_cards = dbc.CardGroup([
    #select magnitude for total count dropdown card
    dbc.Card([
        dbc.CardBody([
            html.H5("Select Magnitude Range:"),
            dcc.Dropdown(options=["1.0 and Higher", "4.0 and Higher", "5.5 and Higher"], value="1.0 and Higher", id="mag-dropdown-tc", style={"color": "black"}),
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
    ])
])



#dropdown cards to provide options for theme and magnitude filter - to be displayed on the left of the visualization
hour_dropdown= dbc.Card([
    dbc.CardBody([
        html.H5("Earthquakes Over the Past Hour"),
        html.Hr(),
        html.Label("Select a Theme:"),
        dcc.Dropdown(options=colours_graph, value="agsunset", id="dropdown-hour-colour", style={'color': 'black'}),
        html.Label("Select Magnitude Range:"),
        dcc.Dropdown(options=["1.0 and Higher", "4.0 and Higher", "5.5 and Higher"], value="1.0 and Higher", id="dropdown-hour-mags", style={"color":"black"}),
    ])
])

day_dropdown= dbc.Card([
    dbc.CardBody([
        html.H5("Earthquakes Over the Past Day"),
        html.Hr(),
        html.Label("Select a Theme:"),
        dcc.Dropdown(options=colours_graph, value="agsunset", id="dropdown-day-colour", style={'color': 'black'}),
        html.Label("Select Magnitude Range:"),
        dcc.Dropdown(options=["1.0 and Higher", "4.0 and Higher", "5.5 and Higher"], value="1.0 and Higher", id="dropdown-day-mags", style={"color":"black"}), 
    ])
])

week_dropdown= dbc.Card([
    dbc.CardBody([
        html.H5("Earthquakes Over the Past 7 Days"),
        html.Hr(),
        html.Label("Select a Theme:"),
        dcc.Dropdown(options=colours_graph, value="agsunset", id="dropdown-week-colour", style={'color': 'black'}),
        html.Label("Select Magnitude Range:"),
        dcc.Dropdown(options=["1.0 and Higher", "4.0 and Higher", "5.5 and Higher"], value="1.0 and Higher", id="dropdown-week-mags", style={"color":"black"}),
    ])
])

month_dropdown= dbc.Card([
    dbc.CardBody([
        html.H5("Earthquakes Over the Past 30 Days"),
        html.Hr(),
        html.Label("Select a Theme:"),
        dcc.Dropdown(options=colours_graph, value="agsunset", id="dropdown-month-colour", style={'color': 'black'}),
        html.Label("Select Magnitude Range:"),
        dcc.Dropdown(options=["1.0 and Higher", "4.0 and Higher", "5.5 and Higher"], value="1.0 and Higher", id="dropdown-month-mags", style={"color":"black"}),
    ])
])




#CREATE INSTANCE OF APP
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server


#APP LAYOUT
app.layout = dbc.Container([
    dbc.Row([
        html.H1(children='Global Earthquake Tracker'),
    ]),
    #displays current eathquake totals
    dbc.Row([
        html.Hr(),
        dashboard_cards,
        html.Hr(),
    ], justify="center"),

    #displays visualizations
    dbc.Tabs([
        dbc.Tab(label="Hour", children=[
            dbc.Row([
                dbc.Col([hour_dropdown], md=3),
                dbc.Col([dcc.Graph(id="plot-hour")], md=9)
            ], align="center", justify="center"),
    ]),
        dbc.Tab(label="Day", children=[
            dbc.Row([
                dbc.Col([day_dropdown], md=3),
                dbc.Col([dcc.Graph(id="plot-day")], md=9)
            ], align="center", justify="center"),
    ]),

        dbc.Tab(label="7 Days", children=[
            dbc.Row([
                dbc.Col([week_dropdown], md=3),
                dbc.Col([dcc.Graph(id="plot-week")], md=9)
            ], align="center", justify="center"),
    ]),

        dbc.Tab(label="30 Days", children=[
            dbc.Row([
                dbc.Col([month_dropdown], md=3),
                dbc.Col([dcc.Graph(id="plot-month")], md=9)
            ], align="center", justify="center"),
    ]),
    ])
], fluid=True)



#CALLBACKS
#total earthquakes counter - update counter based on magnitude range selected by user
@callback(
    Output(component_id= "count-hour", component_property="children"),
    Output(component_id= "count-day", component_property="children"),
    Output(component_id= "count-week", component_property="children"),
    Output(component_id= "count-month", component_property="children"),
    Input(component_id="mag-dropdown-tc", component_property="value")
)
def magnitude_tracker(chosen_mag):
    eq_hour, eq_day, eq_week, eq_month = 0,0,0,0
    if chosen_mag == "1.0 and Higher":
        #eq_count function will filter for earthquakes that fit the magnitude criteria
        #since one feature dictionary = one earthquake, finding the count indicates the earthquake count 
        eq_hour = len(eq_count(0.5,eq_hour_features))
        eq_day = len(eq_count(0.5,eq_day_features))
        eq_week = len(eq_count(0.5,eq_week_features))
        eq_month = len(eq_count(0.5,eq_features))
    elif chosen_mag == "4.0 and Higher":
        eq_hour = len(eq_count(4,eq_hour_features))
        eq_day = len(eq_count(4,eq_day_features))
        eq_week = len(eq_count(4,eq_week_features))
        eq_month = len(eq_count(4, eq_features))
    else:
        eq_hour =len(eq_count(5.5,eq_hour_features))
        eq_day = len(eq_count(5.5,eq_day_features))
        eq_week = len(eq_count(5.5,eq_week_features))
        eq_month = len(eq_count(5.5,eq_features))
    return eq_hour, eq_day, eq_week, eq_month


#VISUALIZATIONS
#earthquakes in the past hour
@callback(
    Output(component_id="plot-hour", component_property="figure"),
    Input(component_id="dropdown-hour-colour", component_property="value"),
    Input(component_id="dropdown-hour-mags", component_property="value"),
)

def hour_figure(chosen_colour, chosen_mag):
        if chosen_mag =="1.0 and Higher":
            if len(mag_hour) != 0:
                fig = px.scatter_mapbox(
                    lon=long_hour,
                    lat=lat_hour,
                    size = mag_hour,
                    color= mag_hour,
                    hover_name = places_hour,
                    color_continuous_scale = chosen_colour,)

            else:
                fig = px.scatter_mapbox(
                    lon=[],
                    lat=[],)
            fig.update_layout(
                mapbox_style="open-street-map")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)")
        elif chosen_mag == "4.0 and Higher":
            if len(mag_hour_4) != 0:
                fig = px.scatter_mapbox(
                    lon=long_hour_4,
                    lat=lat_hour_4,
                    size = mag_hour_4,
                    color= mag_hour_4,
                    hover_name = places_hour_4,
                    color_continuous_scale = chosen_colour,)

            else:
                fig = px.scatter_mapbox(
                    lon=[],
                    lat=[],)
            fig.update_layout(
                mapbox_style="open-street-map")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)")
        else:
            if len(mag_hour_5) != 0:
                fig = px.scatter_mapbox(
                    lon=long_hour_5,
                    lat=lat_hour_5,
                    size = mag_hour_5,
                    color= mag_hour_5,
                    hover_name = places_hour_5,
                    color_continuous_scale = chosen_colour,)

            else:
                fig = px.scatter_mapbox(
                    lon=[],
                    lat=[],)
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)")
            fig.update_layout(
                mapbox_style="open-street-map")
        return fig

#earthquakes in the past day
@callback(
    Output(component_id="plot-day", component_property="figure"),
    Input(component_id="dropdown-day-colour", component_property="value"),
    Input(component_id="dropdown-day-mags", component_property="value"),
)

def day_figure(chosen_colour, chosen_mag):
    if chosen_mag == "1.0 and Higher":
        if len(mag_day) != 0:
            fig = px.scatter_mapbox(
                lon=long_day,
                lat=lat_day,
                size = mag_day,
                color= mag_day,
                hover_name = places_day,
                color_continuous_scale = chosen_colour,)

        else:
            fig = px.scatter_geo(
                lon=[],
                lat=[],)
        fig.update_layout(
                mapbox_style="open-street-map")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)")
    elif chosen_mag == "4.0 and Higher":
        if len(mag_day_4) != 0:
            fig = px.scatter_mapbox(
                lon=long_day_4,
                lat=lat_day_4,
                size = mag_day_4,
                color= mag_day_4,
                hover_name = places_day_4,
                color_continuous_scale = chosen_colour,)
        else:
            fig = px.scatter_mapbox(
                lon=[],
                lat=[],)
        fig.update_layout(
            mapbox_style="open-street-map")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)")
    else:
        if len(mag_day_5) != 0:
            fig = px.scatter_mapbox(
                lon=long_day_5,
                lat=lat_day_5,
                size = mag_day_5,
                color= mag_day_5,
                hover_name = places_day_5,
                color_continuous_scale = chosen_colour,)
        else:
            fig = px.scatter_mapbox(
                lon=[],
                lat=[],)
        fig.update_layout(
                mapbox_style="open-street-map")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)")
    return fig

#earthquakes in the past 7 days
@callback(
    Output(component_id="plot-week", component_property="figure"),
    Input(component_id="dropdown-week-colour", component_property="value"),
    Input(component_id="dropdown-week-mags", component_property="value"),
)

def week_figure(chosen_colour, chosen_mag):
    if chosen_mag == "1.0 and Higher":
        if len(mag_week) != 0:
            fig = px.scatter_mapbox(
                lon=long_week,
                lat=lat_week,
                size = mag_week,
                color= mag_week,
                hover_name = places_week,
                color_continuous_scale = chosen_colour,)
        else:
            fig = px.scatter_mapbox(
                lon=[],
                lat=[],)
        fig.update_layout(
                mapbox_style="open-street-map")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)")

    elif chosen_mag == "4.0 and Higher":
        if len(mag_week_4) != 0:
            fig = px.scatter_mapbox(
                lon=long_week_4,
                lat=lat_week_4,
                size = mag_week_4,
                color= mag_week_4,
                hover_name = places_week_4,
                color_continuous_scale = chosen_colour,)
        else:
            fig = px.scatter_geo(
                lon=[],
                lat=[],)
        fig.update_layout(
                mapbox_style="open-street-map")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)")
    else:
        if len(mag_week_5) != 0:
            fig = px.scatter_mapbox(
                lon=long_week_5,
                lat=lat_week_5,
                size = mag_week_5,
                color= mag_week_5,
                hover_name = places_week_5,
                color_continuous_scale = chosen_colour,)

        else:
            fig = px.scatter_mapbox(
                lon=[],
                lat=[],)
        fig.update_layout(
                mapbox_style="open-street-map")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)")
    return fig



#past 30 days earthquakes
@callback(
    Output(component_id="plot-month", component_property="figure"),
    Input(component_id="dropdown-month-colour", component_property="value"),
    Input(component_id="dropdown-month-mags", component_property="value"),
)

def month_figure(chosen_colour, chosen_mag):
    if chosen_mag == "1.0 and Higher":
        if len(magnitudes) != 0:
            fig = px.scatter_mapbox(
                lon=longitudes,
                lat=latitudes,
                size = magnitudes,
                color= magnitudes,
                hover_name = places,
                color_continuous_scale = chosen_colour,)
        else:
            fig = px.scatter_geo(
                lon=[],
                lat=[],)
        fig.update_layout(
                mapbox_style="open-street-map")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)")

    elif chosen_mag == "4.0 and Higher":
        if len(magnitudes_4) != 0:
            fig = px.scatter_mapbox(
                lon=longitudes_4,
                lat=latitudes_4,
                size = magnitudes_4,
                color= magnitudes_4,
                hover_name = places_4,
                color_continuous_scale = chosen_colour,)
            
        else:
            fig = px.scatter_mapbox(
                lon=[],
                lat=[],
                projection="natural earth")
        fig.update_layout(
                mapbox_style="open-street-map")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)")
    else:
        if len(magnitudes_5) != 0:
            fig = px.scatter_mapbox(
                lon=longitudes_5,
                lat=latitudes_5,
                size = magnitudes_5,
                color= magnitudes_5,
                hover_name = places_5,
                color_continuous_scale = chosen_colour,)
        else:
            fig = px.scatter_geo(
                lon=[],
                lat=[],)
        fig.update_layout(
                mapbox_style="open-street-map")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)")
    return fig


if __name__ == '__main__':
    app.run(debug=True)
