"""
Title: Main
Description: Run and tune main to be sure that everything is running in series.
"""

from vrp import optimise, solution_to_excel
from reframe import reframe_nodes
from plotter import plot_map

do_optimise = True
do_plot = True


def main():

    print("\n" + "="*100 + "\n")

    if do_optimise:
        id_bases = reframe_nodes()
        print("\n" + "=" * 100 + "\n")
        solution = optimise(id_bases)
        print("\n" + "=" * 100 + "\n")
        solution_to_excel(solution)
        if do_plot:
            print("\n" + "=" * 100 + "\n")
            plot_map()


main()
