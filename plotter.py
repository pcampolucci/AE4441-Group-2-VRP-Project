"""
Title: Visual Map of Optimal Solution
Description: The map is interactive and presents ID and status of the bases.
Author: Pietro Campolucci
"""

# import required packages
import pandas as pd
import os
import streamlit as st
import pydeck as pdk

# debugging option
DEBUG = False


def plot_map(path):

    # get databases for initial map and optimal computed solution
    cwd = os.getcwd()
    database = path
    solution = "\database\\solution.xlsx"

    # augment properties of nodes for better understanding of the scenario
    node_dict = {
        'hospital': {'type': 'hospital',
                     'size': 3,
                     'color0': [65, 252, 3],
                     'color1': [252, 186, 3],
                     'color2': [252, 32, 3]},
        'base': {'type': 'base',
                 'size': 5,
                 'color0': [0,0,0]}
    }

    start_df = pd.read_excel(cwd + database)
    start_df['size'] = start_df.apply(lambda row: node_dict[row['type']]['size'], axis=1)
    start_df['color'] = start_df.apply(lambda row: node_dict[row['type']][f'color{row["priority"]}'], axis=1)
    start_df['name'] = start_df['type'] + ' (id: ' + start_df['id'].astype(str) + ')'

    # build data frame for arc plotting based on solution
    solution_df = pd.read_excel(cwd + solution)
    distance_df_adapted = pd.DataFrame(columns=["lng_s", "lat_s", "lng_t", "lat_t"])

    for arc in range(len(solution_df)):
        from_node = start_df.loc[start_df['id'] == solution_df['From'][arc]]
        to_node = start_df.loc[start_df['id'] == solution_df['To'][arc]]
        from_node_lat = from_node["lat"][from_node.index].tolist()[0]
        from_node_long = from_node["long"][from_node.index].tolist()[0]
        to_node_lat = to_node["lat"][to_node.index].tolist()[0]
        to_node_long = to_node["long"][to_node.index].tolist()[0]
        distance_df_row = [from_node_long, from_node_lat, to_node_long, to_node_lat]
        distance_df_adapted.loc[-1] = distance_df_row
        distance_df_adapted.index += 1
        distance_df_adapted = distance_df_adapted.sort_index()

    print("Plotting solution")

    # Build layer for notes plotting
    layer = pdk.Layer(
        "ScatterplotLayer",
        start_df,
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

    # Build layer for path connection, based on solution
    arc_layer = pdk.Layer(
        "ArcLayer",
        data=distance_df_adapted,
        get_width=5,
        get_source_position=["lng_s", "lat_s"],
        get_target_position=["lng_t", "lat_t"],
        get_tilt=15,
        get_source_color=[25, 250, 224],
        get_target_color=[25, 36, 250],
        pickable=False,
        auto_highlight=True,
    )

    # Plot and unify the layers

    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=80.6,
        latitude=7.87,
        zoom=7,
        pitch=50,
        bearing=-20)

    # Combined all of it and render a viewport
    r = pdk.Deck(
        layers=[layer, arc_layer],
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        tooltip={"html": '<b>{type} ID:</b> {id}', "style": {"color": "white"}},
        mapbox_key='pk.eyJ1IjoicGNhbXBvbHVjY2kiLCJhIjoiY2toYTg2bTFxMGg3aTJ5bGhwZWhmMDg0bCJ9.ViTFJLTd8KTj_8MZK0zYWA'
    )

    r.to_html("plots\\routing_solution.html", open_browser=True, notebook_display=False)
    st.pydeck_chart(r)


if DEBUG:
    plot_map("\database\\nodes.xlsx")
