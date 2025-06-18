import json
import sys
from utils.file import load_json
from utils.matrix import add_matrices
from utils.file import input_file

ROUTING = {
    "engine": "ors",
    "profiles": {
        "driving-car": {"host": "localhost", "port": "8080"},
        "driving-hgv": {"host": "localhost", "port": "8080"},
        "cycling-regular": {"host": "localhost", "port": "8080"},
        "cycling-mountain": {"host": "localhost", "port": "8080"},
        "cycling-road": {"host": "localhost", "port": "8080"},
        "cycling-electric": {"host": "localhost", "port": "8080"},
        "foot-walking": {"host": "localhost", "port": "8080"},
        "foot-hiking": {"host": "localhost", "port": "8080"},
    },
}

if __name__ == "__main__":
    inpurt_file = sys.argv[1]
    output_name = input_file[: input_file.rfind(".json")] + "_ors_matrix.json"

    data = load_json(input_file)

    add_matrices(data, ROUTING)

    with open(output_name, "w") as f:
        print("Writing problem with matrix to" + output_name)
        json.dump(data, f, indent=2)