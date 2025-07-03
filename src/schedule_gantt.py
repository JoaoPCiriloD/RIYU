import json
import matplotlib.pyplot as plt
import sys
from utils.color_list import color_list

def plot_schedules(sol_file_name):
    plot_file_name = sol_file_name[0 : sol_file_name.rfind(".json")] + "_gantt.svg"

    print("Parsing" + sol_file_name)
    with open(sol_file_name, "r") as sol_file:
        solution = json.load(sol_file)

    fig, ax1 = plt.subplot(1, 1)
    fig.set_figwidth(15)
    plt.subplost_adjust(left=0.03, right=1, top=1, bottom=0.05, wspace=0.03)

    if "routes" not in solution:
        return
    
    n = len(solution["routes"])
    i = 0

    for route in solution["routes"]:
        color = color_list[route["vehicle"] % len(color_list)]
        t = route["steps"][0]["arrival"]
        d1, d2 = 0, 0
        for step in route["steps"]:
            d1, d2 = d2, step["duration"]
            dt = d2 - d1
            ax1.hlines(
                y=i,
                xmin=t,
                xmax=t + dt,
                colors=color,
            )
            t += dt
            dt = step["waiting_time"]
            t += dt
            dt = step["setup"]
            ax1.hlines(
                y=i,
                xmin=t,
                xmax=t + dt,
                colors=color,
                linewidth=5,
            )
            t += dt
            dt = step["service"]
            if step["type"] in ["job", "pickup", "delivery"]:
                ax1.vlines(
                    x=t,
                    ymin=i - 0.5 + 5 / (n + 10),
                    ymax=i - 0.5 - 5 / (n + 10),
                    colors = color,
                )
                ax1.hlines(
                    y=i,
                    xmin=t,
                    xmax=t + dt,
                    colors = color,
                    linewidth=5,
                )
            elif step["type"] == "break":
                ax1.hlines(
                    y=i,
                    xmin=t,
                    xmax=t + dt,
                    colors=color,
                    linestyle="dashed",
                )