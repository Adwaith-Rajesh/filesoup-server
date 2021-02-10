import os

from flask import Flask, send_file, send_from_directory, abort
from flask_restful import Resource, Api, reqparse

from .server_utils import ServerData
from .server_utils import verify_user
from .server_utils import load_index

app = Flask(__name__)
api = Api(app)

file_index_data = {}

auth_parser = reqparse.RequestParser()
auth_parser.add_argument("username", type=str, required=True, help="username is requires for authentication..")
auth_parser.add_argument("password", type=str, required=True, help="password is required with username for authentication..")

class Indexdata(Resource):
    """Deals with managing the index data that has been generated"""
    

    def get(self):
        """return the entire index data to the client"""
        auth = auth_parser.parse_args()
        if verify_user(username=auth["username"], password=auth["password"]):
            return send_from_directory(os.getcwd(), "file-index.json")
        else:
            abort(401, description="invalid password or username")


class Files(Resource):
    """Allows the client to get the files bases on the id"""

    def get(self, _type: str, _id: str):
        if _type in file_index_data:
            if _id in file_index_data[_type]:
                print('resturning stuff')
                return send_from_directory(file_index_data[_type][_id]["path"], file_index_data[_type][_id]["name"])

            else:
                abort(404, description="The video id does not exists..")

        else:
            abort(404, descripton="The specified type of file cannot be found.")


api.add_resource(Indexdata, "/indexdata")
api.add_resource(Files, "/files/<string:_type>/<string:_id>")

def start_server():
    global file_index_data
    file_index_data = load_index()
    app.run(debug=True, host=ServerData.ip, port=ServerData.port)