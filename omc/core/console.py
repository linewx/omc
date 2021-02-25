import json


class Console:
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    def __init__(self):
        self.level = self.INFO

    def set_level(self, level=INFO):
        self.level = level

    def log(self, message, level=INFO):
        if level >= self.level:
            print(message)
