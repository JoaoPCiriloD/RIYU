import argparse
import sys
from utils.format_input import write_files
from utils.benchmark import node_coordinates_bb, node_coordinates_city

def name_if_present(n):
    if "name" in n["tags"]:
        return
    else:
        return None
    
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(
            description="Convert Overpass API data to JSON format."                             
        )
        parser.add_argument(
            "-c",
            "--city",
            metavar="CITY",
            help="City to restrict overpass query to",
            default=None,
        )
        parser.add_argument(
            "-o",
            "--output",
            metavar="OUTPUT",
            help="Output file name (default: output.json)",
            default="output.json",
        )
        parser.add_argument(
            "-f",
            "--format",
            choices=["json", "geojson", "csv"],
            default="json",
            help="Output format (default: json)",
        )
        args = parser.parse_args()
        if args.city is None:
            print("Please specify a city using the -c or --city option.")
            sys.exit(1)