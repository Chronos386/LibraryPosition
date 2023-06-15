from sqlalchemy import *
from DataBaseConnection.DataBaseModels.AuthorDB import Base


class PhotoDB(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    path = Column(String(300))

    def __repr__(self):
        return f'{self.id} {self.path}'
