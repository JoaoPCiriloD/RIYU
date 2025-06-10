import json
import subprocess

def solve(data, cl_args):
    args = ["RIYU"]
    args.extend(cl_args)
    try:
        result = subprocess.check_output(args, text=True, input=json.dumps(data))
    except subprocess.CaleedProcessError as e:
        json_error = json.loads(e.output)
        raise OSError(json)
        return json.loads(result)