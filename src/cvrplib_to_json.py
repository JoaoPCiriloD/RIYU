import json
import sys
from utils.benchmark import get_value, parse_demand, parse_node_coords, get_matrix

VEHICLE_MARGIR_FACTOR = 1.07

CVRP_FIELDS = [
    "NAME",
    "TYPE",
    "COMMENT",
    "DIMENSION",
    "EDGE_WEIGTH_TYPE",
    "CAPACITY",
    "VEHICLES",
]

def parse_cvrp(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    meta = {}
    for s in CVRP_FIELDS:
        data = get_value(s, lines)
        if data:
            meta[s] = data

    if ("EDGE_WIGHT_TYPE" not in meta) or (meta["EDGE_WEIGHT_TYPE"] != "EUC_2D"):
        message = "Unsupported EDGE_WEIGHT_TYPE"
        if "EDGE_WEIGHT_TYPE" in meta:
            message += ": " + meta["EDGE_WEIGHT_TYPE"]
        message += ","

        print(message)
        exit(0)

    meta["DIMENSION"] = int(meta["DIMENSION"])
    meta["CAPACITY"] = int(meta["CAPACITY"])

    node_start = next(
        
    )