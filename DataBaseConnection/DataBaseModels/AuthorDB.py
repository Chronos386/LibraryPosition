from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AuthorDB(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(300))

    def __repr__(self):
        return f'{self.id} {self.full_name}'
