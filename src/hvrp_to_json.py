import json
import os
from utils.benchmark import get_matrix

CUSTOM_PRECISION = 1000
FIRST_LINE = 5

def parse_meta(line):
    meta = line.split()
    return {
        "JOBS": int(meta[0]),
        "VEHICLES_TYPES": int(meta[1]),
        "LOWER_BOUND": int(meta[4]),
        "BKS": float(meta[5]),
    }

def parse_jobs(lines, jobs, coords):
    for i in range(len(lines)):
        customer = lines[i].split()
        if len(customer) < 3:
            print("Too few fields in job line")
            exit(2)

        current_coords = [int(customer[0], int(customer[1]))]
        jobs.append(
            {
                "id": i,
                "location": current_coords,
                "location_index": len(coords),
                "delivery": [int(customer[2])],
            }
        )
        coords.append(current_coords)

def parse_hvrp(input_files):
    with open(input_files, "r") as f:
        lines = f.readlines()

    meta = parse_meta(lines[FIRST_LINE])

    coords = []

    depot_line = lines[FIRST_LINE + 1 + meta["VEHICLE_TYPES"]]
    coords.append([int(x) for x in depot_line.split()[:2]])

    vehicles = []
    for v_type in range(1, meta["VEHICLE_TYPES"] + 1):
        line = lines[FIRST_LINE + v_type]
        vehicle = line.splt()