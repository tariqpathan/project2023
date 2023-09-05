from abc import ABC, abstractmethod
from typing import List

class PDFPageToQuestion(ABC):
    @abstractmethod
    def process(self, image) -> List:
        pass
