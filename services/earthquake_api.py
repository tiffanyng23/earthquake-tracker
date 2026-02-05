from flask import Flask
import requests
import pandas as pd

# cache earthquake_api
cached = None

def register_cache(cache):
    global cached
    cached = cache

#FUNCTIONS
# get earthquake USGS data using api call 
# convert data to dataframe

# earthquake api call to gather data
def earthquake_data(time_window):
    @cached.memoize(300)
    def fetch_data(time_window):
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
    # return fetch_data since it contains the earthquake data
    return fetch_data(time_window)

#convert json to dataframe
def json_to_df(json_file):
    @cached.memoize(300)
    def convert_data(json_file):
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
        #convert date/time to EST time zone
        df["time"] = df["time"].dt.tz_localize('UTC').dt.tz_convert('America/Toronto')
        # convert time to custom format (year, month, day hour, min, sec)
        df["time"] = df["time"].dt.strftime("%Y-%m-%d %H:%M:%S")

        #convert magnitude to float
        df["magnitude"] = pd.to_numeric(df["magnitude"], downcast="float", errors="coerce")
        return df
    return convert_data(json_file)

#Counts number of earthquakes that meet a specified magnitude threshold
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
