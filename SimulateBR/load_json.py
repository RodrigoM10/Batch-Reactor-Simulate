import json

def load_json_params(filepath="sim_params.json"):
    with open(filepath, "r") as f:
        sim_params = json.load(f)
    return sim_params
