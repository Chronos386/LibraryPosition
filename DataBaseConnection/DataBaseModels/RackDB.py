from sqlalchemy import *
from DataBaseConnection.DataBaseModels.AuthorDB import Base


class RackDB(Base):
    __tablename__ = 'rack'
    id = Column(Integer, primary_key=True)
    x_pos = Column(Float)
    y_pos = Column(Float)

    def __repr__(self):
        return f'{self.id} {self.x_pos} {self.y_pos}'
