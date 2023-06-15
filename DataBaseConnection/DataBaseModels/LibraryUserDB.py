from sqlalchemy import *
from DataBaseConnection.DataBaseModels.AuthorDB import Base


class LibraryUserDB(Base):
    __tablename__ = 'library_user'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    password = Column(String(300))

    def __repr__(self):
        return f'{self.id} {self.name} {self.password}'
