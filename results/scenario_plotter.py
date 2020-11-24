
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

cwd = os.getcwd()

scenario = "\\emergency_solution.csv"

drone_set = set()
drone_id_list = []
base_list = []
time_motion = []
base_prio = [0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2]
new_id = np.arange(1, 14)

with open(cwd+scenario, newline='') as file:
    reader = csv.reader(file, delimiter=' ')
    for i in reader:
        if i[1][2:4] == 'xk':
            drone = i[1].split(",")
            drone_number = drone[0][5:]
            drone_start = drone[1][:-3]
        if i[1][2] == 'x':
            if i[1][2:4] != 'xk':
                base = i[1].split(",")
                start = base[0][4:]
                end = base[1]
                drone_id = base[2][:-3]
        if i[1][2] == 's':
            time = i[1].split(",")
            base_reach = time[0][4:]
            drone_used = time[1][:-2]
            time_taken = i[2][:-4]
            drone_set.add(int(drone_used))
            drone_id_list.append(int(drone_used))
            base_list.append(base_reach)
            time_motion.append(time_taken)

plt.figure()
sns.despine()
sns.color_palette("rocket_r")

for i in drone_set:
    name = "drone " + str(i)
    inx_list = []
    for j in range(len(drone_id_list)):
        if i == drone_id_list[j]:
            inx_list.append(j)

    time_axis = []
    prio_axis = []
    base_list_n = []

    for k in inx_list:
        time_axis.append(float(time_motion[k]))
        prio_axis.append(int(base_prio[k]))
        base_list_n.append(base_list[k])

    for i in range(len(time_axis)):
        plt.annotate(int(base_list_n[i]), [time_axis[i]+0.03, prio_axis[i]+0.03])

    print(time_axis)
    plt.plot(time_axis, prio_axis, marker="o", label=name)


plt.xlabel("Time [min]")
plt.ylabel(f"Priority of Base Reached [/]")
plt.title("Drone Prioritization of Bases")
plt.grid(color='gray', linestyle=':')
plt.legend()
plt.savefig("scenario.png")
plt.show()

