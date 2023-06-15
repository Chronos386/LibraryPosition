import uuid
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from DataBaseConnection.DataBaseModels.BookDB import BookDB
from DataBaseConnection.DataBaseModels.RackDB import RackDB
from DataBaseConnection.DataBaseModels.PhotoDB import PhotoDB
from DataBaseConnection.DataBaseModels.GenreDB import GenreDB
from DataBaseConnection.DataBaseModels.AuthorDB import AuthorDB
from DataBaseConnection.DataBaseModels.UniqueKeyDB import UniqueKeyDB
from DataBaseConnection.DataBaseModels.LibraryUserDB import LibraryUserDB


class DbConnector:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://postgres:Chronos386@localhost/library_pos_db")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def __findFirstFreeID(self, table_db):
        stmt = self.session.query(table_db).order_by(table_db.id.asc()).all()
        count = self.session.query(table_db).count()
        mass = []
        for i in range(1, count + 1):
            if i != stmt[i - 1].id:
                mass.append(i)
        if len(mass) != 0:
            count = mass[0]
        else:
            count += 1
        return count

    def __getCountInTable(self, table_db):
        return self.session.query(table_db).count()

    def __getAllInTable(self, table_db):
        all_entries = self.session.query(table_db).all()
        return all_entries

    def __getEntryById(self, table_db, entry_id):
        entry = self.session.query(table_db).filter_by(id=entry_id).first()
        return entry

    def __addEntry(self, new_entry) -> int:
        self.session.add(new_entry)
        self.session.commit()
        return new_entry.id

    def __updEntry(self, table_db, new_iteration):
        old_iteration = self.session.query(table_db).filter_by(id=new_iteration.id).first()
        old_iteration = new_iteration
        self.session.commit()

    def __delEntry(self, table_db, entry_id: int):
        self.session.query(table_db).filter_by(id=entry_id).delete(synchronize_session=False)
        self.session.commit()

    def getAllUsers(self):
        return self.__getAllInTable(LibraryUserDB)

    def getAllAuthors(self):
        return self.__getAllInTable(AuthorDB)

    def getAllBooks(self):
        return self.__getAllInTable(BookDB)

    def getAllGenres(self):
        return self.__getAllInTable(GenreDB)

    def getAllRacks(self):
        return self.__getAllInTable(RackDB)

    def getRackById(self, id_rack):
        return self.__getEntryById(RackDB, id_rack)

    def loginInDB(self, login: str, password: str):
        acc = self.session.query(LibraryUserDB).filter_by(name=login, password=password).first()
        if acc is None:
            return None
        else:
            key = uuid.uuid4().hex[:30].upper()
            self.session.query(UniqueKeyDB).filter_by(user_id=acc.id).delete(synchronize_session=False)
            new_id = self.__findFirstFreeID(UniqueKeyDB)
            self.__addEntry(UniqueKeyDB(id=new_id, key=key, user_id=acc.id))
            return key

    def addNewAuthor(self, name):
        new_id = self.__findFirstFreeID(AuthorDB)
        return self.__addEntry(AuthorDB(id=new_id, full_name=name))

    def addNewGenre(self, name):
        new_id = self.__findFirstFreeID(GenreDB)
        return self.__addEntry(GenreDB(id=new_id, name=name))

    def addNewPhoto(self, path):
        new_id = self.__findFirstFreeID(PhotoDB)
        return self.__addEntry(PhotoDB(id=new_id, path=path))

    def getPhotoById(self, id_proto):
        return self.__getEntryById(PhotoDB, id_proto)

    def addNewBook(self, name, description, rack_id, auth_id, genre_id, photo_id):
        new_id = self.__findFirstFreeID(BookDB)
        self.__addEntry(BookDB(id=new_id, name=name, description=description, rack_id=rack_id, auth_id=auth_id,
                               genre_id=genre_id, photo_id=photo_id))
