__author__ = 'Jayvee'


class MsgException(Exception):
    def __init__(self, msg):
        self.message = msg