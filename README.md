### Global Earthquake Tracker Dashboard
This is a near live earthquake tracker made using Plotly Dash and the <a href="https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_month.geojson">United States Geological Survey (USGS) earthquake API</a>.

## Project Features
# Earthquake Counter 
There is an earthquake counter spanning the top of the page, providing earthquake counts for the last hour, day, week, month within a chosen magnitude range.

# Customization Panel
On the left side of the app below the Earthquake Counter is a panel to customize the visualizations on the right side.

# Visualizations
The visualizations in this dashboard are a scatter plot, scatter map, and search table. These visualizations are located within the tabs on the dashboard.

# Technologies and Features Implemented
As someone learning more about computer programming/technologies, I wanted to try implementing an API to gather data to create a near real-time tracking tool. I was interested in being able to use the data to create an app that's both interactive and user-driven. This earthquake tracker allows for users to gather specific information they are interested in.

In the future, I hope to implement more detailed information about earthquake events, such as graphing earthquake events by country/region or providing more statistical insights such as: highest/mean magnitude globally or by country, countries/regions with the highest occurences of earthquakes, and visualizations that can filter by country/region. 

## How to Install and Run the Project
Make sure you are connected to the internet since the dashboard fetches data from the USGS API.

1. Clone the repository.
2. Set up a Python virtual environment.
3. Install the packages listed in requirements.txt.
4. Run the app. The app will start a local server which allows for the dashboard to be viewed.

## How to Use the Project
# Earthquake Counter 
 The earthquake counter can be customized to be based on a specified magnitude range. Note that the magnitude range selected is the minimum magnitude (from 0 to 10). After selecting a magnitude range, the earthquake counter will update to count earthquakes at the chosen magnitude and higher.

# Customization Panel
The Customization Panel is used to customize the visualizations within the 3 tabs. The properties that can be customized using this panel are the colour theme for the visualizations (affects the scatter plot and scatter map only), time window (earthquakes within the last hour, day, week, month), and minimum magnitude range (from 0 to 10). This panel is not used for the Earthquake Counter.

# Visualizations
The visualizations are located within the 3 tabs (Scatter Plot of Earthquakes, Scatter Map of Earthquakes, Search for Earthquake) in the dashboard. Click on each tab to view the visualizations. 

Tabs:
Scatter Plot of Earthquakes - contains the scatter plot
Scatter Map of earthquakes - contains the scatter map
Search for Earthquake - contains the search table

Scatter Plot:
The scatter plot graphs earthquake events by time and magnitude. The earthquake events shown can be controlled by the time and magnitude range set in the Customization Panel.

Scatter Map:
The scatter map plots earthquake events on a world map using longitude and latitude data, to identidy the location of the earthquake globally. The earthquake events shown can be controlled by the time and magnitude range set in the Customization Panel.

Search Table:
The search table allows for earthquakes events to be filtered/searched by time, location, and magnitude. Similarly to the scatter plot and map, the initial data in the table can be controlled by the customization panel. The table allows for more precise searching of earthquakes such as for occurences in a specific country, date/time, and magnitude.

# License
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

