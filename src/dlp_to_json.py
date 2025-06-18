import json
import sys
from utils.file import cities_file
CUSTOM_PRECISION = 1000

FIRST_LINE = 5

def parse_meta(line):
    meta = line.split()
    return {"JOBS": int(meta[0]), "VEHICLES_TYPES": int(meta[1])}

def parse_vehicle(line):
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

    meta = parse.
