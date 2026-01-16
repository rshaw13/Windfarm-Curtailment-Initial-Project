import os
import pandas as pd
from utils.scada import get_latest_scada
from utils.weather import get_current_winds
from utils.prediction import load_models, predict
from utils.io import save_live_state

from dotenv import load_dotenv
load_dotenv()

STATIC = pd.read_csv("data/merged_static.csv")

coords = STATIC.set_index("DUID")[["Latitude", "Longitude"]] \
    .agg(lambda r: f"{r[0]},{r[1]}", axis=1).to_dict()

scada = get_latest_scada()
scada_time = scada["SETTLEMENTDATE"].max()

winds = get_current_winds(coords, os.environ["VC_API_KEY"])
models = load_models()
pred = predict(models, winds)

live = STATIC.merge(scada, on="DUID", how="left")
live["predicted_MW"] = live["DUID"].map(pred)
live["scada_timestamp"] = scada_time

save_live_state(live, "data/live_state.parquet")
