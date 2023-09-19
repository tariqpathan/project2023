from abc import ABC, abstractmethod
from typing import Dict

class AbstractAnswerProcessor(ABC):
    EXAM_BOARD = None
    @abstractmethod
    def process(self, *args, **kwargs) -> Dict[int, str]: 
        """Carries out the main processing of the answer sheet"""
        pass