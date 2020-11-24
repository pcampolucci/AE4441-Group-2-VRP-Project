"""
Title: Plotter of Time Taken VS Priority of Base
Author: Pietro Campolucci
"""

# import packages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# read solution time file and specify type of scenario


def time_plot(path, scenario):

    cwd = os.getcwd()
    df = pd.read_excel(cwd + path)

    drone_set = set()
    drone_list = []
    base_list = []
    time_list = []
    prio_list = []

    for base in range(len(df)):

        to_base = df["Target"][base]
        drone = df["Drone ID"][base]
        time = df["Time"][base]
        prio = df["Priority"][base]
        drone_list.append(drone)
        base_list.append(to_base)
        time_list.append(time)
        prio_list.append(prio)
        drone_set.add(drone)

    # plotting solution

    plt.figure()
    sns.despine()

    for i in drone_set:
        name = "drone " + str(i)
        idxs = []
        for j in range(len(drone_list)):
            if i == drone_list[j]:
                idxs.append(j)

        time_axis = []
        prio_axis = []
        base_list_n = []

        for k in idxs:
            time_axis.append(float(time_list[k]))
            prio_axis.append(int(prio_list[k]))
            base_list_n.append(base_list[k])

        for i in range(len(time_axis)):
            plt.annotate(int(base_list_n[i]), [time_axis[i]+0.03, prio_axis[i]+0.03])

        plt.plot(time_axis, prio_axis, marker="o", label=name)

    plt.xlabel("Time [min]")
    plt.ylabel(f"Priority of Base Reached [/]")
    plt.title("Drone Prioritization of Bases")
    plt.grid(color='gray', linestyle=':')
    plt.legend()
    plt.savefig(cwd + f"\\time_plots\{scenario}_scenario.png")

