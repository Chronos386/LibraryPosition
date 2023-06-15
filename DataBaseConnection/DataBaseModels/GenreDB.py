from sqlalchemy import *
from DataBaseConnection.DataBaseModels.AuthorDB import Base


class GenreDB(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))

    def __repr__(self):
        return f'{self.id} {self.name}'
