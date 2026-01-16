import folium

def create_map(df, status_html):
    m = folium.Map(location=[-30, 145], zoom_start=4.5, tiles="CartoDB positron")

    ring_scale = 0.15

    for _, r in df.iterrows():
        folium.CircleMarker(
            location=[r["Latitude"], r["Longitude"]],
            radius=max(r["SCADAVALUE"], 1) * ring_scale,
            fill=True,
            color="green",
            fill_opacity=0.6,
            tooltip=f"{r['Station Name']} — {r['SCADAVALUE']:.1f} MW"
        ).add_to(m)

        folium.CircleMarker(
            location=[r["Latitude"], r["Longitude"]],
            radius=max(r["REG_CAP"], 1) * ring_scale,
            fill=False,
        ).add_to(m)

    m.get_root().html.add_child(folium.Element(status_html))
    return m
