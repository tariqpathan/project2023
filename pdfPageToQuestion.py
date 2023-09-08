from abc import ABC, abstractmethod
from typing import List

class PageProcessor(ABC):
    @abstractmethod
    def process(self, image) -> List:
        pass

class QuestionMetadata(ABC):
    @abstractmethod
    def process(self, image):
        pass

class ConfigValidator(ABC):
    @abstractmethod
    def get_config(self):
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        pass