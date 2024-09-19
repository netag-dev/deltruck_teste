# invalidAuthCodeException.py


class InvalidAuthCodeException(Exception):
    def __init__(self, message):
        super().__init__(message)
