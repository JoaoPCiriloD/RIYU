import argparse
import sys
from utils.format_input import write_files
from utils.benchmark import node_coordinates_bb, node_coordinates_city

def name_if_present(n):
    if "name" in n["tags"]:
        return
    else:
        return None
    
    