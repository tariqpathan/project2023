import logging

from exam_extractor import run_exam_extraction

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("debug-longname.log"),
                              logging.StreamHandler()])

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print("#######---BEGIN---#######")
    logger.info("Starting exam extraction...")
    exam_format = "cambridge_science"
    try:
        run_exam_extraction(exam_format, 'phys-062511-may2016.pdf', 'phys-062511-may2016-ms.pdf')
    except Exception as e:
        logger.exception(e)