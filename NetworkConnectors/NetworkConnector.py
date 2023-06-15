import os
import json
from waitress import serve
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource, reqparse
from RouteFinderA.RouteFinderA import RouteFinderA
from flask import Flask, request, send_file, Response
from DataBaseConnection.DbConnector import DbConnector
from NetworkConnectors.UserModels.SendBook import SendBook
from NetworkConnectors.UserModels.SendGenre import SendGenre
from NetworkConnectors.UserModels.SendAuthor import SendAuthor
from NetworkConnectors.UserModels.SendKey import SendKey, KeysEncoder
from NetworkConnectors.UserModels.SendPictID import SendPictID, PictIdEncoder
from NetworkConnectors.UserModels.SendPoints import SendPoints, PointsEncoder
from NetworkConnectors.UserModels.StartInformModel import StartInformModel, StartEncoder


class RouteResource(Resource):
    def __init__(self):
        self.db_connector = DbConnector()
        self.route_finder = RouteFinderA()
        self.route_finder.init_me()
        self.rout_files = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')

    #  Получение пути
    def get(self, rack_id):
        rack = self.db_connector.getRackById(rack_id)
        path = self.route_finder.start(rack_id)
        final_path = []
        with open(self.rout_files + '/points.json', encoding="utf-8") as json_file:
            points = json.load(json_file)
            for path_point in path:
                for point in points:
                    if point['id'] == path_point:
                        final_path.append(SendPoints(x=point['x'], y=point['y']))
        final_path.append(SendPoints(x=rack.x_pos, y=rack.y_pos))
        data = json.dumps(final_path, cls=PointsEncoder, ensure_ascii=False, sort_keys=True)
        return Response(data, mimetype='application/json')


class StartResource(Resource):
    def __init__(self):
        self.db_connector = DbConnector()
        self.rout_files = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')

    #  Получение начальной информации для приложения
    def get(self):
        books = self.db_connector.getAllBooks()
        books_send = []
        genres = self.db_connector.getAllGenres()
        genres_send = []
        authors = self.db_connector.getAllAuthors()
        authors_send = []
        for book in books:
            photo = self.db_connector.getPhotoById(id_proto=book.photo_id)
            books_send.append(SendBook(id_book=book.id, name=book.name, description=book.description,
                                       rack_id=book.rack_id, auth_id=book.auth_id, genre_id=book.genre_id, photo=photo.path))
        for genre in genres:
            genres_send.append(SendGenre(id_genre=genre.id, name=genre.name))
        for author in authors:
            authors_send.append(SendAuthor(id_auth=author.id, full_name=author.full_name))
        send_data = StartInformModel(all_books=books_send, all_genres=genres_send, all_authors=authors_send)
        data = json.dumps(send_data, cls=StartEncoder, ensure_ascii=False, sort_keys=True)
        return Response(data, mimetype='application/json')


class AdminResource(Resource):
    def __init__(self):
        self.db_connector = DbConnector()

    #  Создание новой книги
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("description", type=str)
        parser.add_argument("rack_id", type=int)
        parser.add_argument("auth_id", type=int)
        parser.add_argument("genre_id", type=int)
        parser.add_argument("photo_id", type=int)
        req = parser.parse_args()
        self.db_connector.addNewBook(name=req.name, description=req.description, rack_id=req.rack_id,
                                     auth_id=req.auth_id, genre_id=req.genre_id, photo_id=req.photo_id)
        return {}, 200


class LoginResource(Resource):
    def __init__(self):
        self.db_connector = DbConnector()

    #  Вход в аккаунт
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("login", type=str)
        parser.add_argument("password", type=str)
        req = parser.parse_args()
        data = self.db_connector.loginInDB(login=req.login, password=req.password)
        if data is None:
            return {}, 404
        else:
            send_data = SendKey(key=data)
            data = json.dumps(send_data, cls=KeysEncoder, ensure_ascii=False, sort_keys=True)
            return Response(data, mimetype='application/json')


class NetworkConnector:
    def __init__(self):
        self.api = Api()
        self.app = Flask(__name__)
        self.dbConnector = DbConnector()
        self.ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
        self.app.secret_key = 'library_pos_key'
        self.app.config['SESSION_TYPE'] = 'filesystem'
        self.app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
        self.app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'photos')
        CORS(self.app)

    def run(self):
        self.__init()
        self.__addURL()
        # self.app.run(port=80, host='192.168.100.3')
        serve(self.app, host="0.0.0.0", port=80)

    def __allowedFile(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def __init(self):
        self.api.add_resource(StartResource, '/api/start/')
        self.api.add_resource(LoginResource, '/api/login/')
        self.api.add_resource(AdminResource, '/api/admin/')
        self.api.add_resource(RouteResource, '/api/route/<int:rack_id>/')
        self.api.init_app(app=self.app)

    def __addURL(self):
        @self.app.route('/api/pictures/', methods=['POST'])
        def saveBookPict():
            if 'file' not in request.files:
                return {}, 400
            file = request.files['file']
            if file.filename == '':
                return {}, 400
            if file and self.__allowedFile(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
                new_id = self.dbConnector.addNewPhoto(path=filename)
                send_data = SendPictID(id_pict=new_id)
                data = json.dumps(send_data, cls=PictIdEncoder, ensure_ascii=False, sort_keys=True)
                return Response(data, mimetype='application/json')

        @self.app.route('/api/map/', methods=['GET'])
        def loadMap():
            filename = "photos\\map.jpg"
            parts = "map.jpg".split(".")
            return send_file(filename, mimetype=f'image/{parts[1]}')

        @self.app.route('/api/pictures/<string:pict_name>/', methods=['GET'])
        def loadPict(pict_name: str):
            filename = "photos\\" + pict_name
            parts = pict_name.split(".")
            return send_file(filename, mimetype=f'image/{parts[1]}')
