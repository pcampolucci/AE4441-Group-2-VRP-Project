import plotly.graph_objects as go
import pandas as pd
import os
import plotly.express as px


cwd = os.getcwd()
database = "\database\\nodes.xlsx"

node_dict = {
    'hospital': {'type': 'hospital', 'size': 3, 'color': 'r'},
    'base': {'type': 'base', 'size': 5, 'color': 'b'}
}

df = pd.read_excel(cwd+database)

df['size'] = df.apply(lambda row: node_dict[row['type']]['size'], axis=1)
df['color'] = df.apply(lambda row: node_dict[row['type']]['color'], axis=1)
df['name'] = df['type'] + ' (id: ' + df['id'].astype(str)

print(df.head())

fig = px.scatter_mapbox(df,
                        lat="lat",
                        lon="long",
                        color="color",
                        hover_name="name",
                        size="size",
                        title="Drone Routing Aegle - Sri Lanka")

fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=7,
                  mapbox_center_lat=7.87,
                  mapbox_center_lon=80.6,
                  margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig.show()