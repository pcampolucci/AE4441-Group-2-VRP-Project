import pandas as pd
import os
import streamlit as st
import pydeck as pdk


cwd = os.getcwd()
database = "\database\\nodes.xlsx"
target = "\database\\pvr_n.xlsx"

df = pd.read_excel(cwd+database)

n = len(df)

distance_df = pd.DataFrame(columns=['From', 'To', 'Distance'])

for i in range(n):
    for j in range(n):
        if i != j:
            from_node = df['id'][i]
            to_node = df['id'][j]
            x_distance = abs(df["lat"][i] - df["lat"][j])*111
            y_distance = abs(df["long"][i] - df["long"][j])*111
            tot_distance = (x_distance ** 2 + y_distance ** 2) ** (1 / 2)
            distance_df.loc[-1] = [from_node, to_node, tot_distance]
            distance_df.index += 1
            distance_df = distance_df.sort_index()

distance_df.to_excel(cwd+target)

#df['size'] = df.apply(lambda row: , axis=1)