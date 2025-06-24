import sys
from utils.file import load_json
from utils.csv_stuff import write_to_csv

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_name = input_file[: input_file.rfind(".json")]

    write_to_csv(load_json(input_file), output_name)