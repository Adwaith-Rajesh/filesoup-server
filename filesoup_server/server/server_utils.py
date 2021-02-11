"""contains extra funcs for app"""


from dataclasses import dataclass
from configparser import ConfigParser
from hashlib import sha256
from typing import Dict
import json


from flask import abort

FileIndexData = Dict[str, Dict[str, str]]


config = ConfigParser()
config.read("./fs_config.cfg")


@dataclass(frozen=True)
class ServerData:

    ip: str = config["server"]["ip"]
    port: int = config["server"]["port"]
    username: str = config["login"]["username"]
    password: str = sha256(
        bytes(config["login"]["password"], encoding="utf8")
    ).hexdigest()


def load_index() -> FileIndexData:
    with open("file-index.json") as f:
        data = json.load(f)

        return data


def verify_user(username: str, password: str) -> bool:
    server_data = ServerData()
    pass_hash = sha256(bytes(password, encoding="utf8")).hexdigest()
    if username == server_data.username and pass_hash == server_data.password:
        return True
    return False


def check_file_exists_on_index_data(data: FileIndexData, _type: str, _id: str) -> int:
    # returns 1 if everything exists
    # returns 2 if _type does not exists
    # returns 3 if _id does not exists
    if _type in data:
        if _id in data[_type]:
            return 1

        else:
            return 2

    else:
        return 3


def dec_verify_user(user_args: Dict[str, str]):
    def in_func(f):
        def wrap(*args, **kwargs):
            if verify_user(
                username=user_args["username"], password=user_args["password"]
            ):
                rv = f(*args, **kwargs)
                return rv

            else:
                abort(404, description="Invalid password or username")

        return wrap

    return in_func
