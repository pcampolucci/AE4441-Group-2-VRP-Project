"""
Title: Mapper of given map for optimiser interpretation.
Description: Mapper of given map for optimiser interpretation.
Author: Pietro Campolucci
"""

# import packages
import pandas as pd
import os

# get files and path information
cwd = os.getcwd()
database = "\database\\nodes.xlsx"
target = "\database\\pvr_n.xlsx"

# build start and end data frames
map_df = pd.read_excel(cwd + database)
distance_df = pd.DataFrame(columns=['From', 'To', 'Distance'])

# compute all possible arcs and respective distance in km
for i in range(len(map_df)):
    for j in range(len(map_df)):
        if i != j:
            from_node = map_df['id'][i]
            to_node = map_df['id'][j]
            x_distance = abs(map_df["lat"][i] - map_df["lat"][j]) * 111
            y_distance = abs(map_df["long"][i] - map_df["long"][j]) * 111
            tot_distance = (x_distance ** 2 + y_distance ** 2) ** (1 / 2)
            distance_df.loc[-1] = [from_node, to_node, tot_distance]
            distance_df.index += 1
            distance_df = distance_df.sort_index()

distance_df.to_excel(cwd+target)
