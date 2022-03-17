import json


def print_json(dict: dict):
    print(json.dumps(dict, indent=4, sort_keys=True))
