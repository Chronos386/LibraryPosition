import json
from NetworkConnectors.UserModels.SendBook import SendBook
from NetworkConnectors.UserModels.SendGenre import SendGenre
from NetworkConnectors.UserModels.SendAuthor import SendAuthor


class StartInformModel:
    def __init__(self, all_books, all_authors, all_genres):
        self.all_books = all_books
        self.all_authors = all_authors
        self.all_genres = all_genres


class StartEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, StartInformModel):
            return obj.__dict__
        if isinstance(obj, SendBook):
            return obj.__dict__
        if isinstance(obj, SendGenre):
            return obj.__dict__
        if isinstance(obj, SendAuthor):
            return obj.__dict__
        return super().default(obj)
