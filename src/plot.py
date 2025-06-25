import json
import matplotlib.pyplot as plt
import sys
from utils.color_list import color_list

TASKS_TYPES = ["job", "pickup", "delivery"]

def plot_routes(solution, plot_base_name):
    fig, ax1 = plt.subplots(1, 1)
    fig.set_figwidth(15)
    plt.subplots_adjust(left=0.03, right=1, top=1, bottom=0.05, wspace=0.03)

    if "routes" not in solution:
        return
    
    first_start = solution["routes"][0]["steps"][0]["location"]
    first_end = solution["routes"][0]["steps"][-1]["location"]

    xmin = min(first_start[0], first_end[0])
    xmax = xmin
    ymin = min(first_start[1], first_end[1])
    ymax = ymin

    vehicles_have_same_start_end = (len(solution["routes"]) > 1)
    for route in solution["routes"]:
        current_start = route["steps"][0]["location"]
        current_end = route["steps"][-1]["location"]

        if current_start != first_start or current_end != first_end:
            vehicles_have_same_start_end = False
            break

    for route in solution["routes"]:
        lons = [
            step["locations"][0]
            for step in route["steps"]
            if not vehicles_have_same_start_end or step["type"] in TASKS_TYPES
        ]
        lats = [
            step["locations"][1]
            for step in route["steps"]
            if not vehicles_have_same_start_end or step["type"] in TASKS_TYPES
        ]

        ax1.plot(lons, lats, color=color_list[route["vehicle"] % len(color_list)])

        bbox = [[min(lons), min(lats)], [max(lons), max[lats]]]

        xmin = min(xmin, bbox[0][0])
        xmax = max(xmax, bbox[1][0])
        ymin = min(ymin, bbox[0][1])
        ymax = max(ymax, bbox[1][1])


        step = route["steps"][-1]
        if step["type"] == "end":
            ax1.scatter(
                [step["location"][0]], [step["location"][1]], color="red", linewidth=8
            )

        step = route["steps"][0]
        if step["type"] == "start":
            ax1.scatter(
                [step["location"][0]], [step["location"][1]], color="green", linewidth=1 
            )

        for step in route["steps"]:
            if step["type"] == "job":
                marker_shape = "o"
                marker_color = "blue"
            elif step["type"] == "pickup":
                marker_shape = 