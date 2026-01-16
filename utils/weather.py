import pandas as pd
import requests
from io import StringIO

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

def get_current_winds(coords: dict, api_key: str):
    winds = {}

    for duid, loc in coords.items():
        params = {
            "unitGroup": "metric",
            "elements": "windspeed",
            "include": "current",
            "key": api_key,
            "contentType": "csv"
        }

        r = requests.get(f"{BASE_URL}/{loc}", params=params)
        df = pd.read_csv(StringIO(r.text))
        winds[duid] = df.loc[0, "windspeed"] * 0.277778  # km/h → m/s

    return winds
