import json


class SendPictID:
    def __init__(self, id_pict):
        self.id = id_pict


class PictIdEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SendPictID):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
