import os
import json
from pathlib import Path

def get_config_pathname():
    dir_path = Path(__file__).parent
    file_location = "config.json"
    config_path = os.path.join(dir_path, file_location)
    incorrect_path = os.path.join(dir_path, "wrong")

    with open(config_path, 'r') as f:
        config = json.load(f)
        print(config)

    with open(incorrect_path, 'r') as f:
        incorrect_config = json.load(f)
        print(config)


if __name__ == "__main__":
    get_config_pathname()