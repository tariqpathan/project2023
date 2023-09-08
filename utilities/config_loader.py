import json
import os
from exceptions import InvalidConfigurationException
from pathlib import Path

def load_config():
    current_directory = Path.cwd()
    filename = os.environ.get('config_location', 'config.json')
    loc = Path.joinpath(current_directory, filename)
    with open(loc, 'r') as f:
        config_data = json.load(f)
    return config_data

def get_config(data, mode):
    return data[mode]

def validate_config(config):
    if not config['cambridge_science']['subjects']: raise InvalidConfigurationException('subjects not valid', None)
    # other validations here

if __name__ == "__main__":
    data = load_config()
    print(get_config(data, 'cambridge_science'))
    validate_config(data) # needs cambridge_science