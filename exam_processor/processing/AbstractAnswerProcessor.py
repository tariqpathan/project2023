from abc import ABC, abstractmethod

class AbstractAnswerProcessor(ABC):
    EXAM_BOARD = None
    @abstractmethod
    def process(self, *args, **kwargs): 
        """Carries out the main processing of the answer sheet"""
        pass