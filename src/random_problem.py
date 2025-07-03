import argparse
import numpy.random as npr
from utils.format_input import write_files

def generate_random_problem(j, s, v, center, sw, ne, file_name, uniform, geojson, csv):
    locations = {}

    if uniform:
        if center:
            v_loc = [(sw[0] + ne[0]) / 2, (sw[1] + ne[1]) / 2]
        else:
            v_lon = round(npr.uniform(sw[0], ne[0], 1)[0], 5)
            v_lat = round(npr.uniform(sw[1], ne[1], 1)[0], 5)
            v_loc = [v_lon, v_lat]

        locations["vehicles"] = {"coordinates": [v_loc] * v}

        locations["jobs"] = {"coordinates": []}
        for i in range(j):
            j_lon = round(npr.uniform(sw[0], ne[0], 1)[0], 5)
            j_lat = round(npr.uniform(sw[1], ne[1], 1)[0], 5)
            locations["jobs"]["coordinates"].append([j_lon, j_lat])

        locations["shipments"] = {"coordinates": []}
        for i in range(2 * s):
            s_lon = round(npr.uniform(sw[0], ne[0], 1)[0], 5)
            s_lat = round(npr.uniform(sw[1], ne[1], 1)[0], 5)
            locations["shipments"]["coordinates"].append([s_lon, s_lat])

    else:
        mu_lon = (sw[0] + ne[0]) / 2
        mu_lat = (sw[1] + ne[1]) / 2
        sigma_lon = (ne[0] - mu_lon) / 3
        sigma_lat = (ne[1] - mu_lat) / 3

        if center:
            v_loc = ()
        else:
            v_lon = round(npr.normal(mu_lon, sigma_lon, 1)[0], 5)
            v_lat = round(npr.normal(mu_lat, sigma_lat, 1)[0], 5)
            v_loc = [v_lon, v_lat]

        locations["vehicles"] = {"coordinates": [v_loc] * v}

        locations["jobs"] = {"coordinates": []}

        for i in range(j):
            j_lon = round(npr.normal(mu_lon, sigma_lon, 1)[0], 5)
            j_lat = round(npr.normal(mu_lat, sigma_lat, 1)[0], 5)
            locations["jobs"]["coordinates"].append([j_lon, j_lat])
        
        locations["shipments"] = {"coordinates": []}

        
         
        