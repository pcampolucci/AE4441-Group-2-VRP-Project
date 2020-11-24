"""
Title: Main
Description: Run and tune main to be sure that everything is running in series.
"""

from vrp import optimise
from reframe import reframe_nodes
from map_plotter import plot_map
from verification_plotter import simpleplot
from reframe_solution import solution_to_excel
from time_plotter import time_plot

do_reframe = False  # only for debugging reframe (keep False)
do_optimise = True
do_plot = True
do_simple_plot = False
wind_speed = 14  # [m/s]
scenario = "basic"
is_mac = False

if is_mac:
    nodes_path = "/database/validation.xlsx"
    time_path = "/database/solution_time.xlsx"
else:
    nodes_path = "\database\\nodes.xlsx"  # use the tiny version for testing (nodes.xlsx default)
    time_path = "\\database\\solution_time.xlsx"


def main():

    print("\n" + "="*100 + "\n")

    if do_reframe:
        reframe_nodes(is_mac, nodes_path, wind_speed)

    if do_optimise:
        id_bases = reframe_nodes(is_mac, nodes_path, wind_speed)
        print("\n" + "=" * 100 + "\n")
        solution, fullsolution = optimise(id_bases, is_mac)
        print("\n" + "=" * 100 + "\n")
        solution_to_excel(is_mac, solution, fullsolution)
        if do_plot:
            print("\n" + "=" * 100 + "\n")
            plot_map(nodes_path, is_mac)
            time_plot(time_path, scenario)
        if do_simple_plot:
            print("\n" + "=" * 100 + "\n")
            simpleplot()


main()
