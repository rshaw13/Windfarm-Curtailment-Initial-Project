import pandas as pd
import requests
import zipfile
import io

BASE_URL = "https://www.nemweb.com.au/REPORTS/CURRENT/Dispatch_SCADA/"

def get_latest_scada():
    index = requests.get(BASE_URL).text
    zip_name = sorted(
        [l.split('"')[1] for l in index.splitlines() if "DISPATCHSCADA" in l]
    )[-1]

    url = f"{BASE_URL}{zip_name}"
    resp = requests.get(url)

    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f)

    df.columns = df.iloc[0]
    df = df.iloc[1:-1][["SETTLEMENTDATE", "DUID", "SCADAVALUE"]]
    df["SCADAVALUE"] = pd.to_numeric(df["SCADAVALUE"])
    df["SETTLEMENTDATE"] = pd.to_datetime(df["SETTLEMENTDATE"])

    return df
