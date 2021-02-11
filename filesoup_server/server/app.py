import os
from requests.api import post

import werkzeug
from flask import Flask, send_file, send_from_directory, abort
from flask_restful import Resource, Api, reqparse

from filesoup_server.files.file_manager import check_file_exists
from .server_utils import ServerData
from .server_utils import verify_user
from .server_utils import load_index
from .server_utils import dec_verify_user
from .server_utils import check_file_exists_on_index_data

app = Flask(__name__)
api = Api(app)

file_index_data = {}


# normal authentication parser
auth_parser = reqparse.RequestParser()
auth_parser.add_argument(
    "username",
    type=str,
    required=True,
    help="username is required for authentication..",
)
auth_parser.add_argument(
    "password",
    type=str,
    required=True,
    help="password is required with username for authentication..",
)

# post requests parser
post_parser = reqparse.RequestParser()
post_parser.add_argument(
    "file",
    type=werkzeug.datastructures.FileStorage,
    required=True,
    help="The type of the file to be written is requires...",
    location="files",
)


class Indexdata(Resource):
    """Deals with managing the index data that has been generated"""

    def get(self):
        @dec_verify_user(auth_parser.parse_args())
        def in_get():
            return send_from_directory(os.getcwd(), "file-index.json")

        return in_get()


class Files(Resource):
    """Allows the client to get the files bases on the id"""

    def get(self, _type: str, _id: str):
        @dec_verify_user(auth_parser.parse_args())
        def in_get():
            cv = check_file_exists_on_index_data(
                data=file_index_data, _type=_type, _id=_id
            )
            if cv:
                return send_from_directory(
                    file_index_data[_type][_id]["path"],
                    file_index_data[_type][_id]["name"],
                )

            elif cv == 2:
                abort(404, descripton="The specified type of file cannot be found.")

            elif cv == 3:
                abort(404, description="The video id does not exists..")

        return in_get()

    def delete(self, _type: str, _id: str):
        @dec_verify_user(auth_parser.parse_args())
        def in_delete():
            cv = check_file_exists_on_index_data(
                data=file_index_data, _type=_type, _id=_id
            )
            if cv:
                # TODO: remove the id from the index data, delete the file from the file system
                pass
            elif cv == 2:
                pass

            elif cv == 3:
                pass

    def post(self, _type: str, _id: str):
        auth = auth_parser.parse_args()
        post_args = post_parser.parse_args()
        _file = post_args["file"]
        _file.save("return_data.mp4")


api.add_resource(Indexdata, "/indexdata")
api.add_resource(Files, "/files/<string:_type>/<string:_id>")


def start_server():
    global file_index_data
    file_index_data = load_index()
    app.run(debug=True, host=ServerData.ip, port=ServerData.port)
