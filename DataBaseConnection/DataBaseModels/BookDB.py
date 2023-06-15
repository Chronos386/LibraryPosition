from sqlalchemy import *
from DataBaseConnection.DataBaseModels.AuthorDB import Base


class BookDB(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    description = Column(String(600))
    rack_id = Column(Integer, ForeignKey('rack.id'))
    auth_id = Column(Integer, ForeignKey('author.id'))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    photo_id = Column(Integer, ForeignKey('photo.id'))

    def __repr__(self):
        return f'{self.id} {self.name} {self.description} {self.rack_id} {self.auth_id} {self.genre_id} {self.photo_id}'
