"""
Title: Main
Description: Run and tune main to be sure that everything is running in series.
"""

from vrp import optimise, solution_to_excel
from reframe import reframe_nodes
#from plotter import plot_map

do_reframe = False  # only for debugging reframe (keep False)
do_optimise = True
do_plot = False
wind_speed = 0  # [m/s]

ismac = True
if ismac:
    #nodes_path = "/database/nodes.xlsx"
    nodes_path = "/database/validation.xlsx"
else:
    nodes_path = "\database\\nodes.xlsx"  # use the tiny version for testing (nodes.xlsx default)


def main():

    print("\n" + "="*100 + "\n")

    if do_reframe:
        reframe_nodes(ismac,nodes_path, wind_speed)

    if do_optimise:
        id_bases = reframe_nodes(ismac,nodes_path, wind_speed)
        print("\n" + "=" * 100 + "\n")
        solution = optimise(id_bases)
        print("\n" + "=" * 100 + "\n")
        solution_to_excel(ismac,solution)
        if do_plot:
            print("\n" + "=" * 100 + "\n")
            plot_map(nodes_path)


main()
