from dash import Dash, html, dash_table, dcc, callback, Output, Input
from flask import Flask
from flask_caching import Cache
import requests
import plotly.express as px
import dash_bootstrap_components as dbc

#CREATE INSTANCE OF APP
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server
#cache
cache = Cache(app.server, config={
    'CACHE_TYPE': 'SimpleCache',  
    'CACHE_DEFAULT_TIMEOUT': 300  #cache timeout in seconds
})

#FUNCTIONS
#get earthquake data using api call
#all earthquakes worldwide within a specified time period
@cache.memoize(timeout=300)
def earthquake_data(time_window):
    url = f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_{time_window}.geojson"
    try:
        response = requests.get(url)
        #converts json text to python dictionary
        data = response.json()
        #extract earthquake features key
        earthquake_features = data["features"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching earthquake data: {e}")
        earthquake_features = []
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        earthquake_features = []

    return earthquake_features

#Counts number of earthquakes that meet a specified magnitude threshold
@cache.memoize(timeout=300)
def eq_count(magnitude_limit, earthquake_list=[]):
    # convert magnitude selected from dropdown to a float
    magnitude_limit =float(magnitude_limit)
    counter=0

    for earthquake in earthquake_list:
        mag = earthquake["properties"].get("mag")
        # in case magnitude is not recorded
        if mag is not None and float(mag)>= magnitude_limit:
            counter+=1
    return counter


#COLOURS FOR VISUALIZATIONS
#colour scales for graphs
colours_graph = px.colors.named_colorscales()


#CARDS 
#Summary dashboard showing total earthquakes over the past hour, day, week, month
#create 4 cards for total count - to be displayed underneath the title
summary_dashboard = dbc.CardGroup([
    #select magnitude for total count dropdown card
    dbc.Card([
        dbc.CardBody([
            html.H5("Select Magnitude Range:"),
            dcc.Dropdown(options=["1.0", "4.0", "5.5"], value="1.0", id="summary-magnitude", style={"color": "black"}),
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

#dropdown cards to provide options for theme and magnitude filter
customize_dashboard = dbc.Card([
     dbc.CardBody([
        html.H5("Customize Your Earthquake Visual"),
        html.Hr(),
        html.Label("Select a Theme:"),
        dcc.Dropdown(options=colours_graph, value="agsunset", id="dropdown-colour", style={'color': 'black'}),
        html.Label("Select a Time Period:"),
        dcc.Dropdown(options=["hour", "day", "week", "month"], value="month", id="dropdown-time", style={'color': 'black'}),
        html.Label("Select a Minimum Magnitude Range:"),
        dcc.Dropdown(options=["1.0", "4.0", "5.5"], value="1.0", id="dropdown-magnitude", style={"color":"black"}),
    ])
 ])



#APP LAYOUT
app.layout = dbc.Container([
    dbc.Row([
        html.H1(children='Global Earthquake Tracker', className="text-center"),
    ]),

    #displays current eathquake totals
    dbc.Row([
        html.Hr(),
        summary_dashboard,
        html.Hr(),
    ], justify="center"),

    #displays visualizations
    dbc.Row([
            dbc.Col([customize_dashboard], md=3),
                dbc.Col([dcc.Graph(id="final-plot")], md=9)
            ], align="center", justify="center"),
], fluid=True)


#CALLBACKS
#Summary dashboard
@callback(
    Output(component_id= "count-hour", component_property="children"),
    Output(component_id= "count-day", component_property="children"),
    Output(component_id= "count-week", component_property="children"),
    Output(component_id= "count-month", component_property="children"),
    Input(component_id="summary-magnitude", component_property="value")
)
def summary_tracker(magnitude):
    magnitude = float(magnitude) 
    eq_totals = {"hour":0, "day":0, "week":0, "month":0}

    for time in eq_totals.keys():
        #api request, collect earthquake data for specified time thresholds (hour, day, month, week)
        raw_features = earthquake_data(time)
        # count earthquakes that fit each time window and magnitude, update dictionary values
        eq_totals[time] = eq_count(magnitude, raw_features)
    # return each of the values
    return eq_totals["hour"], eq_totals["day"], eq_totals["week"], eq_totals["month"]


#VISUALIZATIONS
#earthquakes visual based on theme, time, and magnitude
@callback(
    Output(component_id="final-plot", component_property="figure"),
    Input(component_id="dropdown-colour", component_property="value"),
    Input(component_id="dropdown-time", component_property="value"),
    Input(component_id="dropdown-magnitude", component_property="value"),
)
def earthquake_figure(colour, time, magnitude):
    #api request - pull earthquakes for specified time window
    raw_features = earthquake_data(time)
    
    #filter earthquakes in selected time window that fit magnitude threshold
    filtered_features =[]
    for earthquake in raw_features:
        if float(earthquake["properties"]["mag"]) >= float(magnitude):
            filtered_features.append(earthquake)

    # display map with earthquakes
    if len(filtered_features) != 0:
        fig = px.scatter_mapbox(
            # loop through features list to get feature for each earthquake
            lon= [eq["geometry"]["coordinates"][0] for eq in filtered_features],
            lat= [eq["geometry"]["coordinates"][1] for eq in filtered_features],
            size = [eq["properties"]["mag"] for eq in filtered_features],
            color= [eq["properties"]["mag"] for eq in filtered_features],
            hover_name = [eq["properties"]["place"] for eq in filtered_features],
            color_continuous_scale = colour,)
    else:
        fig = px.scatter_mapbox(
            lon=[],
            lat=[],)
    
    fig.update_layout(
        mapbox_style="open-street-map",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
