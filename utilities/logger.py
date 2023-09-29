import logging
from termcolor import colored

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'WARNING': 'yellow',
        'INFO': 'cyan',
        'DEBUG': 'green',
        'CRITICAL': 'red',
        'ERROR': 'red'
    }

    def format(self, record):
        log_message = super(ColoredFormatter, self).format(record)
        return colored(log_message, self.COLORS.get(record.levelname))

def setup_logging():
    formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])