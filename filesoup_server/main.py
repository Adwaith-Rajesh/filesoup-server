from .files.file_indexer import index_files
from .server.app import start_server


def start_service():
    index = index_files()

    if index:
        start_server()