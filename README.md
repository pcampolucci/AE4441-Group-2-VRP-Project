# AE4441-Group-2-VRP-Project

The tool solves a typical vehicle routing problem. In this scenario, we have a number of delivery drones located at a 
number of bases in the country of reference. In the simulated scenario, we want to deliver a certain amount of blood 
to each hospital in the area in the fastest possible way, in the more efficient way. 

The features of this tool are:

- Multiple starting bases
- Priority setting for each hospital based on the urgency 
- Wind effect on the speed of the drone
- Max drone range constraint

![cover](https://i.imgur.com/poZbiU0.png)

## Infrastructure

The code is organized as follows:

- The various nodes and their features are inserted in `database/nodes.xlsx`
- Nodes and additional factors (e.g. wind) are coupled and translated into edge variables with `reframe.py`
- The Mixed Integer Programming model is defined and solved through Gurobi in `vrp.py`
- The solution is translated and plotted alongside the nodes in a MapBox plot with `plotter.py`
- A 2D conventional plot of the solution can also be created with `verification_plotter.py`

The various processes can be tuned and run in series safely in `main.py`. This allows to avoid any conflict in the 
compilation.

## Dependencies

- Gurobipy
- Pydeck
- Streamlit


