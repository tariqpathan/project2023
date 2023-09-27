class InvalidConfigurationException(BaseException):
    def __init__(self, message, errors):
        super().__init__(message)
