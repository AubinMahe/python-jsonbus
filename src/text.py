import time


class Text:

    def __init__(self, text: str = ''):
        self.time = 0
        self.text = text

    def set_time(self, time: float = time.time()):
        self.time = time
