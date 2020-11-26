"""
Title: Build solution files for postprocessing
Author: Pietro Campolucci
"""

# import packages
import pandas as pd
import os

# get directory path
cwd = os.getcwd()


def solution_to_excel(ismac, solution, fullsolution):

    solution_df = pd.DataFrame(columns=["From", "To", "Drone"])
    time_solution_df = pd.DataFrame(columns=["Drone ID", "Target", "Time", "Priority"])

    if ismac:
        solution_path = "/database/solution.xlsx"
        time_solution_path = "/database/solution_time.xlsx"
        priority_path = "/database/nodes.xlsx"
    else:
        solution_path = "\database\solution.xlsx"
        time_solution_path = "\database\solution_time.xlsx"
        priority_path = "\database\\nodes.xlsx"

    # retrieve information for path plotter and write this to "data"
    for edge in solution:
        if str(edge[0][:2]) != 'xk':
            if str(edge[0][:1]) != 's':
                i_clean = edge[0][2:-1].split(",")
                from_node = i_clean[0]
                to_node = i_clean[1]
                drone_id = i_clean[2]
                solution_df.loc[-1] = [from_node, to_node, drone_id]
                solution_df.index += 1
                solution_df = solution_df.sort_index()
                solution_df = solution_df.iloc[::-1]

    solution_df.to_excel(cwd + solution_path, 'data')

    # retrieve time information for plotter
    prio_df = pd.read_excel(cwd + priority_path)

    for i in fullsolution:
        base_to_reach = int(i[0].split(",")[0][2:])
        drone_used = int(i[0].split(",")[1][:-1])
        time_to_reach = float(i[1])
        priority_base = prio_df.loc[prio_df['id'] == base_to_reach, 'priority'].item()
        time_solution_df.loc[-1] = [drone_used, base_to_reach, time_to_reach, priority_base]
        time_solution_df.index += 1
        time_solution_df = time_solution_df.sort_index()
        time_solution_df = time_solution_df.iloc[::-1]

    time_solution_df.to_excel(cwd + time_solution_path, 'data')
    print("Solution written to ", cwd + solution_path)
    print("Solution for Time written to ", cwd + time_solution_path)
