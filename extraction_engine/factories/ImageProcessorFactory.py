from extraction_engine.processing.AbstractImageProcessor import AbstractImageProcessor
from extraction_engine.processing.CambridgeScienceImageProcessor import CambridgeScienceImageProcessor

class ImageProcessorFactory:
    @staticmethod
    def create_processor(exam_format: str, config) -> AbstractImageProcessor:
        # A dictionary to map EXAM_FORMAT values to their respective classes
        processor_map = {
            "cambridge_science": CambridgeScienceImageProcessor,
        }
        # Fetch the appropriate class based on the exam_format string
        processor_class = processor_map.get(exam_format)
        
        if not processor_class:
            raise ValueError(f"No processor found for exam board '{exam_format}'")
        else:
            return processor_class(config)