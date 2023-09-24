import logging
import time
from create_test_db import load_db, delete_db, delete_images
from exam_extractor import run_exam_extraction

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("debug-longname.log"),
                              logging.StreamHandler()])

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    delete_images()
    print("#######---BEGIN---#######")
    logger.info("Starting exam extraction...")
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