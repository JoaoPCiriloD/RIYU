import json
import sys
from utils.file import cities_file
CUSTOM_PRECISION = 1000

FIRST_LINE = 5

def parse_meta(line):
    meta = line.split()
    return {"JOBS": int(meta[0]), "VEHICLES_TYPES": int(meta[1])}

def parse_depot(line):
    depot = line.split()
    return int(depot[0]), 
    
def parse_matrix(lines):
    N = len(lines)
    matrix = []
    for line in lines:
        current_line = [int(v) for v in line.split()]
        if len(current_line) != N:
            print("Matrix problem")
            exit(1)

        matrix.append(current_line)
    return matrix

def parse_jobs(lines, cities, jobs):
    for i in range(len(lines)):
        customer = lines[i].split()
        if len(customer) < 2:
            print("Too few fields in job line", i)
            exit(2)

        index = int(customer[0])

        jobs.append(
            {
                "id": index,
                "description": cities[index]["description"],
                "location": cities[index]["location"],
                "location_index": index,
                "delivery": [int(customer[1])],
            }
        )

def get_cities(cities_lines):
    with open(cities_lines, "r") as c:
        lines = c.readlines()

    cities = []

    for line in lines[1:]:
        fields = line.split(",")
        cities.append({
            "description": fields[0],
            "location":[
            float(fields[2]),
            float(fields[1]),
            ],
         }
        )

    return cities

def parse_dlp(input_file, cities_lines):
    with open(input_file, "r") as f:
        lines = f.readlines()

    cities = get_cities(cities_lines)

    meta = parse_meta(lines[FIRST_LINE])

    instance_name = input_file[: input_file.rfind(".")]
    BKS = {
        instance_name: {
            "class": "DLP",
            "best_known_cost": 0,
            "jobs": meta["JOBS"],
            "total_demand": 0,
            "total_capacity": 0,
            "vehicles": 0,
        }
    }
    depot_index = parse_depot(lines[FIRST_LINE + meta["VEHICLES_TYPES"] + 1])

    matrix_start = FIRST_LINE + meta["VEHICLES_TYPES"] + 2
    matrix = parse_matrix(lines[matrix_start : matrix_start + meta["JOBS"] + 1])

    vehicles = []

    for v_type in range(1, meta["VEHICLES_TYPES"] + 1):
        line = lines[FIRST_LINE + v_type]
        vehicle = line.split()

        v_number = int(vehicle[0])
        v_capacity = int(vehicle[1])
        v_fixed_cost = int(CUSTOM_PRECISION * float(vehicle[2]))
        v_du_cost = float(vehicle[3]) 

        BKS[instance_name]["vehicles"] += v_number
        BKS[instance_name]["total_capacity"] += v_number * v_capacity

        for n in range(v_number):
            vehicles.append(
                {
                    "id": v_type * 1000 + n,
                    "start": cities[0]["location"],
                    "start_index": depot_index,
                    "end": cities[0]["location"],
                    "end_index": depot_index,
                    "capacity": [v_capacity],
                    "costs": {"fixed": v_fixed_cost, "per_hour": int(3600 * v_du_cost)},
                    "description": str(v_type),
                }
            )