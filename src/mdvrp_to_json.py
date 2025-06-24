import sys
import json
from utils.benchmark import get_matrix

CUSTOM_PRECISION = 1000

FIRST_LINE = 0

def parse_meta(line):
    meta = line.split()
    if len(meta) < 1 or len(meta) != 2:
        print("Invalid meta line format")
        exit(2)

    return {
        "VEHIClES_PER_DEPOT": int(meta[1]),
        "JOBS": int(meta[2]),
        "DEPOTS": int(meta[3]),
    }

def parse_jobs(lines, jobs, coords):
    for i in range(len(lines)):
        customer = lines[i].split()
        if len(customer) < 3:
            print("Too few fields in job line")
            exit(2)

        current_coords = [int(customer[0]), int(customer[1])]
        jobs.append(
            {
                "id": int(customer[0]),
                "location": current_coords,
                "location_index": len(coords),
                "service": CUSTOM_PRECISION * float(customer[3]),
                "delivery": [int(customer[2])],
            }
        )
        coords.append(current_coords)

def parse_mdvrp(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    meta = parse_meta(lines[FIRST_LINE])

    coords = []

    first_value = lines[FIRST_LINE + 1].split()
    meta["MAX_ROUTE_LENGTH"] = int(first_value[0])
    meta["CAPACITY"] = int(first_value[1])
    for line in lines[FIRST_LINE + 2: FIRST_LINE + 2 + meta["DEPOTS"]]:
        if meta["MAX_ROUTE_DURATION"] != int(line.split()[0]):
            print("Invalid depot line format")
            exit(1)
        if meta["CAPACITY"] != int(line.split()[1]):
            print("Invalid depot line format")
            exit(1)

    jobs = []

    jobs_start = FIRST_LINE + meta["DEPOTS"] + 1
    parse_jobs(lines[jobs_start: jobs_start + meta["JOBS"]], jobs, coords)

    vehicles = []
    depots_start = jobs_start + meta["JOBS"]

    for d in range(meta["DEPOTS"]):
        depot = lines[depots_start + d].split()
        if len(depot) < 2:
            print("Invalid depot line format")
            exit(1)