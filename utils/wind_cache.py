import pandas as pd
from pathlib import Path
import requests
from io import StringIO

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

CACHE_DIR = Path("data/wind_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_historical_wind(
    duid: str,
    location: str,
    first_date: str,
    last_date: str,
    api_key: str
):
    """
    Loads wind data from cache if available, otherwise fetches and caches.
    """
    cache_file = CACHE_DIR / f"{duid}_{first_date}_{last_date}.parquet"

    if cache_file.exists():
        return pd.read_parquet(cache_file)

    params = {
        "unitGroup": "metric",
        "elements": "datetime,windspeed",
        "include": "hours",
        "key": api_key,
        "contentType": "csv"
    }

    url = f"{BASE_URL}/{location}/{first_date}/{last_date}"
    r = requests.get(url)
    r.raise_for_status()

    df = pd.read_csv(StringIO(r.text))
    df["datetime"] = pd.to_datetime(df["datetime"]).dt.floor("h")
    df["windspeed"] = df["windspeed"] * 0.277778

    df.to_parquet(cache_file, index=False)
    return df
