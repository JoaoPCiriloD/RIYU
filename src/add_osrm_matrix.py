import json
import sys
from utils.file import load_json
from utils.matrix import add_matrices
from utils.file import input_file

ROUTING = {
    "engine": "osrm",
    "profiles": {
        "car": {"host": "localhost", "port": "5000"},
        "hgv": {"host": "localhost", "port": "5000"},
        "bike": {"host": "localhost", "port": "5000"},
        "foot": {"host": "localhost", "port": "5000"},
    },
}

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_name = input_file[: input_file.rfind(".json")] + "_osrm_matrix.json"

    data = load_json(input_file)

    add_matrices(data, ROUTING)

    with open(output_name, "w")as out:
        print("Writing problem with matrix to" + output_name)
        json.dump(data, out, indent=2)