import json
from pathlib import Path

def load_data(json_path : Path):
    if json_path.exists():
        with open(json_path, "r") as f:
            return json.load(f)
    else:
        return []
    
def save_data(json_path : Path, file_list : list):
    with open(json_path, "w") as f:
        json.dump(file_list,f)