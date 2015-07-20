__author__ = 'Jayvee'


class MsgException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message

    def __unicode__(self):
        return self.message
