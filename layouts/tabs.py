import dash_bootstrap_components as dbc
from dash import Dash, dash_table, dcc
from dash.dash_table.Format import Format, Scheme

def tabs_layout():
    return dcc.Tabs(
        id="main-tabs",
        value="tab-1",
        children=[
            dcc.Tab(
                label="Scatter Map of Earthquakes", 
                value="tab-1",
                children=[
                    dcc.Graph(id="scatter-map")
                ],
                className ="tab-btn", 
                selected_className="tab-btn--selected", 
            ),
            dcc.Tab(
                label="Scatter Plot of Earthquakes", 
                value="tab-2",
                children=[
                        dcc.Graph(id="scatter-plot")
                ],
                className ="tab-btn", 
                selected_className="tab-btn--selected", 
            ),
            dcc.Tab(
                label="Search for Earthquakes", 
                value="tab-3",
                children=[
                        dash_table.DataTable(
                            id="summary-table", # from callback output,has the data and columns
                            filter_action="native",
                            sort_action="native", # user is allowed to sort columns
                            sort_mode="multi", # sort multiple columns at once
                            style_data={
                                "color": "rgba(0,0,0,1)",
                                "backgroundColor": "rgba(220,220,220,1)"
                            },
                            style_header={
                                "color": "rgba(255,255,255,1)",
                                "backgroundColor": "rgba(0,0,0,1)",
                            },
                            style_table={"overflowX": "auto"},
                            style_cell={'padding': '5px', "textAlign": "left"},
                            filter_options={"placeholder_text": "Type Input to Filter"},
                            page_size=10,
                        ),
                    ],
                className ="tab-btn", 
                selected_className="tab-btn--selected", 
            ),
        ]
    )