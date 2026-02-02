import dash_bootstrap_components as dbc
from dash import html, dcc

#CARDS 
#Summary dashboard showing total earthquakes over the past hour, day, week, month
#create 4 cards for total earthquake count (month, week, day, hour)

def summary_dashboard():
    return dbc.CardGroup([
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
