import json
import sys
from utils.benchmark import get_matrix


CUSTOM_PRECISION = 1000

def parse_meta(line):
    x = line.split()
    if len(x) < 2:
        print("Cannot undestand meta linde: too few columns.")
        exit(2)

    return {"VEHICLES": int(x[0]), "CAPACITY": int(x[1])}

def parse_jobs(line, pickups, deliveris, coords):
    x = line.split()
    if len(x) < 9:
        print("Cannot undestand job line: too few columns.")
        exit(2)

    job = {
           "id": int(x[0]),
        "location": [float(x[1]), float(x[2])],
        "location_index": len(coords),
        "amount": [int(float(x[3]))],
        "time_windows": [
            [CUSTOM_PRECISION * int(float(x[4])), CUSTOM_PRECISION * int(float(x[5]))]
        ],
        "service": CUSTOM_PRECISION * int(float(x[6])),
    }
    coords.append([float(x[1]), float(x[2])])

    pickup_id = int(x[7])
    delivery_id = int(x[8])