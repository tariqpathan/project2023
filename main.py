import logging
import time
from create_test_db import load_db, delete_db, delete_images
from extraction_engine.extract import run_exam_extraction

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("debug-longname.log"),
                              logging.StreamHandler()])

logger = logging.getLogger(__name__)


def get_mode():
    input_str = input("""
    Select from the following options:\n
    1: Run exam extraction\n
    2: Retrieve questions\n
    3: Run a machine learning process\n
    4: Exit\n                   
    """)
    try: 
        input_mode = int(input_str)
    except ValueError:
        print("Please enter a valid number")
        return get_mode()



if __name__ == "__main__":
    delete_images()
    print("#######---BEGIN---#######")
    session = load_db()
    exam_format = "cambridge_science"
    try:
        run_exam_extraction(exam_format, 'bio-may2010.pdf', 'bio-may2010-ms.pdf')
    except Exception as e:
        logger.exception(e)
    
    finally:
        # delete_db(session)
        # time.sleep(10)
        # delete_images()
        print("#######---END---#######")