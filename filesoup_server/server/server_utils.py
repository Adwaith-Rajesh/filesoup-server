"""contains extra funcs for app"""


from dataclasses import dataclass
from configparser import ConfigParser
from hashlib import sha256
from typing import Dict
import json


FileIndexData = Dict[str, Dict[str, str]]


config = ConfigParser()
config.read("./fs_config.cfg")

@dataclass(frozen=True)
class ServerData:

    ip: str = config["server"]["ip"]
    port: int = config["server"]["port"]
    username: str = config["login"]["username"]
    password: str = sha256(bytes(config["login"]["password"], encoding="utf8")).hexdigest()


def load_index()-> FileIndexData:
    with open("file-index.json") as f:
        data = json.load(f)

        return data


def verify_user(username: str, password: str) -> bool:
    server_data = ServerData()
    pass_hash = sha256(bytes(password, encoding="utf8")).hexdigest()
    if username == server_data.username and pass_hash == server_data.password: return True
    return False