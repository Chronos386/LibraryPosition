import json


class SendPoints:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PointsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SendPoints):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
