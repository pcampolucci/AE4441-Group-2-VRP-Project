"""
Title: Mapper of given map for optimiser interpretation.
Description: Mapper of given map for optimiser interpretation.
Author: Pietro Campolucci
"""

# import packages
import numpy as np
from math import *
import pandas as pd
import os


def reframe_nodes(is_mac, path, V_wind=2):

    # get files and path information
    cwd = os.getcwd()
    database = path
    if is_mac:
        target = "/database/variables.xlsx"
    else:
        target = "\database\\variables.xlsx"

    print("Reading nodes and bases from ", cwd+database)

    # build start and end data frames
    map_df = pd.read_excel(cwd + database)
    distance_df = pd.DataFrame(columns=['From', 'To', 'Distance', 'Priority', "DeltaV"])
    id_bases = []
    count_bases = 1

    # compute all possible arcs and respective distance in km
    for i in range(len(map_df)):
        if map_df['type'][i] == 'base':
            id_bases.append(count_bases)
            count_bases += 1
        for j in range(len(map_df)):
            if i != j:
                from_node = map_df['id'][i]
                to_node = map_df['id'][j]
                x_distance = abs(map_df["lat"][i] - map_df["lat"][j]) * 111
                y_distance = abs(map_df["long"][i] - map_df["long"][j]) * 111
                tot_distance = (x_distance ** 2. + y_distance ** 2.) ** (1. / 2.)
                priority = map_df['priority'][i]
                delta_lat = map_df["lat"][j] - map_df["lat"][i]
                delta_long = map_df["long"][j] - map_df["long"][i]
                if V_wind==0:
                    Delta_V = 0
                else:
                    angle = np.arctan((delta_lat / delta_long)) * 360 / 2 / pi
                    angle_wind = angle + 90
                    factor = np.cos(angle_wind * 2 * pi / 360)
                    Delta_V = (V_wind * factor)/3.6
                distance_df.loc[-1] = [from_node, to_node, tot_distance, priority, Delta_V]
                distance_df.index += 1
                distance_df = distance_df.sort_index()
                distance_df = distance_df.iloc[::-1]

    distance_df.to_excel(cwd+target, 'data')

    print(distance_df.head())
    print("\nExcel file written in ", cwd+target, "\nIDs of bases: ", id_bases)
    return id_bases
