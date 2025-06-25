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

def parse_depot(line):
    x = line.split()
    if len(x) < 3:
        print("Cannot undestand depot line: too few columns.")
        exit(2)

    return {
        "location": [int(x[1]), int(x[2])],
        "time_windows": [CUSTOM_PRECISION * int(float(x[4])), CUSTOM_PRECISION * int(float(x[5]))]
    }

def parse_jobs(line, pickups, deliveries, coords):
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

    if pickup_id == 0:     
        job["matching_delivery"] = delivery_id
        pickups.append(job)

    else:
        if delivery_id != 0:
            print("Invalid job line: both pickup and delivery ids are not zero.")
            exit(2)
            
        job["matching_pickup"] = pickup_id
        deliveries[x[0]] = job

    def parse_pdptw(input_file):
        with open(input_file, "r") as f:
            lines = f.readlines()

        meta = parse_meta(lines[0])
        meta["NAME"] = input_file

        depot = parse_depot(lines[1].strip())

        coords = [depot["location"]]

        vehicles = []
        for v in range(meta["VEHICLES"]):
            vehicles.append(
                {
                    "id": v,
                    "start": depot["location"],
                    "start_index": 0,
                    "end": depot["location"],
                    "end_index": 0,
                    "capacity": [meta["CAPACITY"]],
                    "time_windows": depot["time_windows"],
                }
            )
        
        pickup = []
        deliveris = {}

        for line in lines[2:]:
            parse_jobs(line, pickups, deliveries, coords)

        meta["JOBS"] = len(pickups) + len(deliveries)

        shipments = []

        for pickup in pickups:
            delivery = deliveries.get(pickup["matching_delivery"])
            if (delivery["matching_pickup"] != pickup["id"]) or (
                delivery["amount"][0] != -pickup["amount"][0]
            ):
                print("Invalid job line: pickup and delivery do not match.")
                exit(2)

        matrix = get_matrix(coords, CUSTOM_PRECISION)

        return {
            "meta": meta,
            "vehicles": vehicles,
            "shipments": shipments,
            "matrices": {"car": {"durations": matrix}},
        }
    
    if __name__ == "__main__":
     input_file = sys.argv[1]
     output_name = input_file[: input_file.rfind(".")] + ".json"

    print("- Writing problem " + input_file + " to " + output_name)
    json_input = parse_pdptw(input_file)

    with open(output_name, "w") as out:
        json.dump(json_input, out)