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
            v_loc = [v_lon, v_lat]

            