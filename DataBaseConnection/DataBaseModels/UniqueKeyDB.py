from sqlalchemy import *
from DataBaseConnection.DataBaseModels.AuthorDB import Base


class UniqueKeyDB(Base):
    __tablename__ = 'unique_key'
    id = Column(Integer, primary_key=True)
    key = Column(String(300))
    user_id = Column(Integer, ForeignKey('library_user.id'))

    def __repr__(self):
        return f'{self.id} {self.key} {self.user_id}'
