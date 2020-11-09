import pandas as pd
import os
import streamlit as st
import pydeck as pdk


cwd = os.getcwd()
database = "\database\\nodes.xlsx"

node_dict = {
    'hospital': {'type': 'hospital', 'size': 3, 'color': [255, 140, 0]},
    'base': {'type': 'base', 'size': 5, 'color': [0, 255, 255]}
}

df = pd.read_excel(cwd+database)

df['size'] = df.apply(lambda row: node_dict[row['type']]['size'], axis=1)
df['color'] = df.apply(lambda row: node_dict[row['type']]['color'], axis=1)
df['name'] = df['type'] + ' (id: ' + df['id'].astype(str) + ')'

print(df.head())

layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=100,
    radius_min_pixels=10,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position="[long, lat]",
    get_radius="exits_radius",
    get_fill_color="color",
    get_line_color=[0, 0, 0],
)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=80.6,
    latitude=7.87,
    zoom=7,
    pitch=50,
    bearing=-20)

# Combined all of it and render a viewport
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"html": '<b>Node ID:</b> {id}', "style": {"color": "white"}},
    mapbox_key='pk.eyJ1IjoicGNhbXBvbHVjY2kiLCJhIjoiY2toYTg2bTFxMGg3aTJ5bGhwZWhmMDg0bCJ9.ViTFJLTd8KTj_8MZK0zYWA'
)
r.to_html("plots\\test.html", open_browser=True, notebook_display=False)
st.pydeck_chart(r)

