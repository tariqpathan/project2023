from functools import lru_cache

import yaml

from fastapi import HTTPException

from database.database_manager import DatabaseManager
from extraction_engine.managers.file_manager import FileManager


DATABASE_KEY = "db_path" # Name of the key that stores the database path in the config file
UPLOADS_KEY = "uploads"
EXAM_CONFIG_KEY = "config"

db_path = FileManager.get_filepaths(DATABASE_KEY)
uploads_path = FileManager.get_filepaths(UPLOADS_KEY)
config_path = FileManager.get_filepaths(EXAM_CONFIG_KEY)

# for imports
db_manager = DatabaseManager(db_path)

@lru_cache(maxsize=1)
def load_exam_formats():
    try:
        with config_path.open('r') as f:
            config_data = yaml.safe_load(f)
        exam_formats = list(config_data.get("exam_formats", {}).keys())
        return exam_formats
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Exam format configuration file not found")
    except yaml.YAMLError:
        raise HTTPException(status_code=500, detail="Failed to parse the YAML file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unknown error occurred: {e}")