from dash import Dash, html, dash_table, dcc, callback, Output, Input
from flask import Flask
from flask_caching import Cache
import requests
import pandas as pd
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
#get earthquake data using api call and convert data to dataframe
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

#convert json to dataframe
@cache.memoize(timeout=300)
def json_to_df(json_file):
    # create dictionary for each earthquake, store as a list of dictionaries
    data_for_df = []

    for eq in json_file:
        # check that there is required data for each earthquake
        if eq.get("properties") and eq.get("geometry"):
            eq_dict = {
                "id": eq["id"],
                "magnitude": eq["properties"].get("mag"),
                "place": eq["properties"].get("place"),
                "time": eq["properties"].get("time"),
                "longitude": eq["geometry"]["coordinates"][0],
                "latitude": eq["geometry"]["coordinates"][1],
                "depth": eq["geometry"]["coordinates"][2],
            }
        # append each dictionary to data_for_df list
        data_for_df.append(eq_dict)

    #convert data_for_df to a df
    df = pd.DataFrame(data_for_df)
    # convert magnitude from string to float and time to datetime format
    df["time"] = pd.to_datetime(df["time"], unit="ms", errors="coerce")
    df["magnitude"] = pd.to_numeric(df["magnitude"], downcast="float", errors="coerce")
    return df

#Counts number of earthquakes that meet a specified magnitude threshold
@cache.memoize(timeout=300)
def eq_count(magnitude_limit, earthquake_list=[]):
    # convert magnitude selected from dropdown to a float
    magnitude_limit =float(magnitude_limit)
    counter=0

    for earthquake in earthquake_list:
        mag = earthquake["properties"].get("mag")
        # in case magnitude is not recorded
        if mag is not None and float(mag) >= magnitude_limit:
            counter+=1
    return counter


#extract data for dash table
table_data = earthquake_data("month")
table_data = json_to_df(table_data)
table_data = table_data[["time", "place", "magnitude"]]


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
            html.H5("Minimum Magnitude:", className="text-center"),
            html.Br(),
            dcc.Slider(0, 10, 1, value=5, marks=None,
                tooltip={"placement": "bottom", "always_visible": True}, 
                id="summary-magnitude"),
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

#dropdown cards to provide options for theme, time and magnitude filter
customize_dashboard = dbc.Card([
     dbc.CardBody([
        html.H5("Customize Your Earthquake Visual"),
        html.Hr(),
        html.Label("Theme:"),
        dcc.Dropdown(options=colours_graph, value="agsunset", id="dropdown-colour", style={'color': 'black'}),
        html.Label("Time Window:"),
        dcc.Dropdown(options=["hour", "day", "week", "month"], value="month", id="dropdown-time", style={'color': 'black'}),
        html.Br(),
        html.Label("Minimum Magnitude:"),
        dcc.Slider(0, 10, 1, value=5, marks=None,
                tooltip={"placement": "bottom", "always_visible": True}, 
                id="slider-magnitude"),
    ])
 ])

#APP LAYOUT
app.layout = dbc.Container([
    dbc.Row([
        html.H1(children='Global Earthquake Tracker', className="text-center"),
    ]),

    #displays earthquake counter
    dbc.Row([
        html.Hr(),
        summary_dashboard,
        html.Hr(),
    ], justify="center"),

    #displays visualizations
    dbc.Row([
        dbc.Col([customize_dashboard], md=3),
        dbc.Col([
            dcc.Tabs([
                dcc.Tab(label="Scatter Map of Earthquakes", children=[
                    dcc.Graph(id="scatter-map")
                ]),
                dcc.Tab(label="Scatter Plot of Earthquakes", children=[
                    dcc.Graph(id="scatter-plot")
                ]),
                dcc.Tab(label="Search for Earthquakes by Location", children=[
                    dash_table.DataTable(
                        data = table_data.to_dict("records"),
                        columns = [{'name': i, 'id': i, "deletable": False, "editable" : False} for i in table_data.columns],
                        filter_action="native",
                        filter_options={"placeholder_text": "Filter column..."},
                        page_size=10,
                    ),
                ])
            ])
        ], md=9)
    ], align="center", justify="center")
], fluid=True),



#CALLBACKS
#Summary dashboard
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


#visualizations
#earthquakes visual based on theme, time, and magnitude
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
        color_continuous_scale = colour)
    
    fig.update_layout(
        map_style="open-street-map",
        paper_bgcolor="rgba(0,0,0,0)", 
        dragmode="zoom",
    )
    return fig

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
    return fig


if __name__ == '__main__':
    app.run(debug=True)
