import requests
import plotly.express as px
import pandas as pd


#creating earthquake tracker webpage - below are code to be used in the app
#will use these plots to make a plotly dash app

#use for loop to loop through each dictionary in eq_features to extract magnitude, coordinates, place 
#create function to extract specified features
def extract_features(features, places, magnitudes, longitudes, latitudes):
    for eq in features:
        place = eq["properties"]["place"]
        mag = eq["properties"]["mag"]
        long = eq["geometry"]["coordinates"][0]
        lat = eq["geometry"]["coordinates"][1]
        places.append(place)
        magnitudes.append(mag)
        longitudes.append(long)
        latitudes.append(lat)
    return places, magnitudes, longitudes, latitudes



#api for all earthquakes worldwide in the past month with a magnitude of 1.0 or higher
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_month.geojson"

#sending api request
response = requests.get(url)
response_dict = response.json()
response_dict["metadata"]["status"]
#status code is 200, meaning that the api call was successful

#4 main categories: type, metadata, features, bbox
response_dict.keys()

#get info about api call
response_dict["metadata"]
#9268 earthquakes from the past month

#Collect features data
eq_features = response_dict["features"]

#extract specified features
magnitudes, places, longitudes, latitudes = [],[],[],[]
month_eq = extract_for_plot(eq_features, magnitudes, places, longitudes, latitudes)


#worldwide earthquakes for the past 7 days with a magnitude of 1.0 or higher
url_2 = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.geojson"

#api call
response_2 = requests.get(url_2)
#convert to dictionary
response_2_dict = response_2.json()

#api call was successful
print(f"status: {response_2_dict['metadata']['status']}")

#number of earthquakes
response_2_dict["metadata"]["count"]

#extract features for each earthquake
eq_week_features = response_2_dict["features"]

#extract place, magnitude, coordinates
places_week, mag_week, long_week, lat_week = [], [], [], []
week_eq = extract_for_plot(eq_week_features, places_week, mag_week, long_week, lat_week )


#earthquakes for the past day
url_day = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_day.geojson"

#api call
response_day = requests.get(url_day)
#convert to dictionary
response_day = response_day.json()
print(f"status code: {response_day['metadata']['status']}")

#number of earthquakes
response_day["metadata"]["count"]

#extract features for each earthquake
eq_day_features = response_day["features"]

#extract place, magnitude, coordinates
places_day, mag_day, long_day, lat_day = [], [], [], []
day_eq = extract_for_plot(eq_day_features, places_day, mag_day, long_day, lat_day)



#earthquakes for the past hour
url_hour = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_hour.geojson"

#api call
response_hour = requests.get(url_hour)
#convert to dictionary
response_hour = response_hour.json()
print(f"status code: {response_hour['metadata']['status']}")

#number of earthquakes
response_hour["metadata"]["count"]

#extract features for each earthquake
eq_hour_features = response_hour["features"]

#extract place, magnitude, coordinates
places_hour, mag_hour, long_hour, lat_hour = [], [], [], []
results = extract_for_plot(eq_hour_features, places_hour, mag_hour, long_hour, lat_hour)


#visualizations for App:
fig = px.scatter_geo(
    lon=longitudes,
    lat=latitudes,
    size = magnitudes,
    hover_name = places,
    title = f"Worldwide Earthquakes Over the Past 30 Days",
    color_continuous_scale = "blugrn",
    projection="natural earth",)
fig.show()



fig = px.scatter_geo(
    lon=long_week,
    lat=lat_week,
    size = mag_week,
    hover_name = places_week,
    title = f"Worldwide Earthquakes Over the Past 7 Days",
    color_continuous_scale = "blugrn",
    projection="natural earth",)
fig.show()



fig = px.scatter_geo(
    lon=long_day,
    lat=lat_day,
    size = mag_day,
    hover_name = places_day,
    title = f"Worldwide Earthquakes Over the Past Day",
    color_continuous_scale = "blugrn",
    projection="natural earth",)
fig.show()




fig = px.scatter_geo(
    lon=long_hour,
    lat=lat_hour,
    size = mag_hour,
    hover_name = places_hour,
    title = f"Worldwide Earthquakes Over the Past Hour",
    color_continuous_scale = "blugrn",
    projection="natural earth",)
fig.show()

#NEW ADDITION FOR APP
#want to be able to adjust dataset based on magnitude: 1, 4, 6
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

#specifically extract earthquakes with a magnitude over 6
magnitudes, places, longitudes, latitudes = [],[],[],[]
results = extract_spec_features(5.5, eq_features, places, magnitudes, longitudes, latitudes)

#earthquake total count based on magnitude
eq_count_4=[]
def eq_count(magnitude_limit, features=[]):
    eq_count=[]
    for eq in features:
        if eq["properties"]["mag"] >= magnitude_limit:
            eq_count.append(eq)
    return eq_count
eq_count_4 = eq_count(6, eq_day_features)
        
len(eq_count_4)









