import json
from utils.csv_stuff import write_csv_header

def format_json_from_locations(location):
    instance = {"vehicles": []}
    for i in range(len(location["vehicles"]["coordinates"])):
        instance["vehicles"].append(
            {
                "id": i,
                "start": location["vehicles"]["coordinates"][i],
                "end": location["vehicles"]["coordinates"][i],
            }       
        )
        
        if("names" in location["vehicles"]) and (
            location["vehicles"]["names"] is not None
        ):
            
            instance["vehicles"][-1]["name"] = location["vehicles"][
                "names"
            ][i]
            instance["vehicles"][-1]["endDescription"] = location["vehicles"]["names"][i]

    job_coords = []
    if ("jobs" in location) and (len(location["jobs"]["coordinates"]) > 0):
        job_coords = location["jobs"]["coordinates"]
        instance["jobs"] = []

    j = len(job_coords)
    for i in range(j):
        current = {"id": i + 1, "location": job_coords[i]}
        if ("names" in location["jobs"]) and (
            location["jobs"]["names"] is not None
        ):
            current["decription"] = location["jobs"]["names"][i]
        instance["jobs"].append(current)

    shipment_coords = []
    if ("shipments" in location) and (len(location["shipments"]["coordinates"]) > 0):
        shipment_coords = location["shipments"]["coordinates"]
        instance["shipments"] = []

    s = len(shipment_coords)
    for i in range(s):
        current = {
            "pickup": {"id": j + 2 * i + 1, "location": shipment_coords[2 * i]},
            "delivery": {"id": j + 2 * i + 2, "location": shipment_coords[2 * i + 1]},
        }
        if "names" in location["shipments"]:
            if location["shipments"]["name"][2 * i] is not None:
                current["pickup"]["description"] = location["shipments"]["names"][2 * i]
            if location["shipments"]["names"][2 * i + 1] is not None:
                current["delivery"]["description"] = location["shipments"]["names"][2 * i + 1]
        instance["shipments"].append(current)

    return instance

def format_geojson_from_locations(location):
    geo_content = {"type": "FeatureCollection", "features": []}

    for key in location:
        for i in range(len(location[key]["coordinates"])):
            feature = {
                "type": "Feature",
                "properties": {
                    "id": i,
                    "name": location[key]["names"][i] if "names" in location[key] else None,
                    "type": key,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": location[key]["coordinates"][i],
                },
            }
            if ("names" in location[key]) and (location[key]["names"][i] is not None):
                # Override if name is known
                current = ["properties"]["name"] = location[key]["names"][i]

            geo_content["features"].append(current)

    return geo_content

def write_files(file_name, location, geojson, csv):
    json_input = format_json_from_locations(location)

    with open(file_name + ".json", "w") as out:
        print("Writing problem to" + file_name + ".json")
        json.dump(json_input, out, indent=4)
    if geojson:
        with open(file_name + ".geojson", "w") as out:
            print("Writing problem to " + file_name + ".geojson")
            json.dump(format_geojson_from_locations(location), out, indent=2)
    
    if csv:
        writse_to_csv(file_name, json_input)