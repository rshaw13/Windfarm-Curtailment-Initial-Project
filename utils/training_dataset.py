import pandas as pd
from utils.wind_cache import get_historical_wind


def build_training_dataset(
    daily_scada: dict,
    wf_coords: dict,
    api_key: str,
    first_date: str,
    last_date: str
):
    """
    Build aligned SCADA + windspeed datasets per windfarm.
    """

    # 1️⃣ Combine all SCADA data
    scada_all = pd.concat(daily_scada.values())
    scada_all.index = pd.to_datetime(scada_all.index)
    scada_all = scada_all.sort_index()

    combined = {}

    # 2️⃣ LOOP OVER EACH WINDFARM  ← ← ← HERE
    for duid, location in wf_coords.items():

        # Skip if SCADA not available
        if duid not in scada_all.columns:
            continue

        # 3️⃣ GET WIND DATA (CACHED)  ← ← ← THIS IS THE BIT YOU ASKED ABOUT
        wind = get_historical_wind(
            duid=duid,
            location=location,
            first_date=first_date,
            last_date=last_date,
            api_key=api_key
        )

        # 4️⃣ PREPARE SCADA DATA
        scada = (
            scada_all[[duid]]
            .reset_index()
            .rename(columns={"index": "datetime", duid: "output MW"})
        )
        scada["datetime"] = pd.to_datetime(scada["datetime"]).dt.floor("h")

        # 5️⃣ MERGE WIND + SCADA
        merged = pd.merge(
            wind[["datetime", "windspeed"]],
            scada,
            on="datetime",
            how="inner"
        )

        combined[duid] = merged

    return combined
