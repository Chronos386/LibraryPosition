import json


class SendKey:
    def __init__(self, key):
        self.key = key


class KeysEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SendKey):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
