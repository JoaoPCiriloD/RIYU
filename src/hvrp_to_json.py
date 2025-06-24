import json
from utils.benchmark import get_matrix
import sys

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

        v_number = int(vehicle[0])
        v_capacity = int(vehicle[1])
        v_fixed_cost = int(CUSTOM_PRECISION * float(vehicle[2]))
        v_du_cost = float(vehicle[3]) 

        for n in range(v_number):
            vehicles.append(
                {
                    "id": v_type * 1000 + n,
                    "start": coords[0],
                    "start_index": 0,
                    "end": coords[0],
                    "end_index": 0,
                    "capacity": [v_capacity],
                    "costs": {"fixed": v_fixed_cost, "per_hour":  int(3600 * v_du_cost)},
                    
                }
            )

    jobs = []
    jobs_start = FIRST_LINE + 1 + meta["VEHICLE_TYPES"] + 2
    parse_jobs(lines[jobs_start: jobs_start + meta["JOBS"]], jobs, coords)

    matrix = get_matrix(coords, CUSTOM_PRECISION)

    meta["VEHICLES"] = len(vehicles)

    return {
        "meta": meta,
        "vehicles": vehicles,
        "jobs": jobs,
        "matrices": {"car": {"duration": matrix}},
    }

if __name__ == "__main__":
    input_file = sys.argv[1]
    instance_name = input_file[: input_file.rfing(".txt")]
    output_name = instance_name + ".json"

    json_input = parse_hvrp(input_file)

    json_input["meta"]["instance_name"] = instance_name

    with open(output_name, "w") as out:
        json.dump(json_input, out)
