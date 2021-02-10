from configparser import ConfigParser
from pathlib import Path
import json
import uuid
import mimetypes

from typing import List
from typing import Dict
import os

from colorama import Fore
import colorama

from .file_utils import filter_list


colorama.init()

# Types
FileIndexData = Dict[str, Dict[str, str]]


def make_json_file(data: FileIndexData):
    with open("./file-index.json", "w") as index_file:
        json.dump(data, index_file)

def prepare_index_data(indexed_files: List[str]) -> FileIndexData:
    print("\033[39m")
    """This will prepare the file-index.json file"""
    temp_index = {}
    for filename_with_path in indexed_files:
        filename = os.path.basename(filename_with_path)
        _type = mimetypes.guess_type(filename_with_path)[0].split("/")[0]

        file_data = {
            "name": filename,
            "path": os.path.dirname(filename_with_path)
        }

        def gen_id():
            nonlocal temp_index
            _id = uuid.uuid4().hex[:8]
            if _id in temp_index:
                gen_id()
            return _id

        file_data_id = gen_id()

        if not _type in temp_index:
            temp_index[_type] = {}
            
        temp_index[_type][file_data_id] = file_data

    return temp_index


def get_files(dirs: List[str]) -> List[str]:
    """Gets all the files from the given dirs and indexes them"""

    indexed_files = []
    print()
    print(f"{Fore.GREEN}Indexing Files...")

    for _dir in dirs:
        if Path(_dir).is_dir():
            for dir_name, _, filenames in os.walk(_dir):
                print(f"{Fore.BLUE}Indexed '{dir_name}'")
                for filename in filenames:
                    indexed_files.append(os.path.join(dir_name, filename))

        else:
            print(f"{Fore.YELLOW}skipping '{_dir}' as the directory does not exists.")

    return indexed_files


def index_files(force_index: bool=False) -> bool:
    """indexes all the files from the given directories."""
    if not Path("./file-index.json").is_file() or force_index:  # checks whether an index already exists or not
        config = ConfigParser()
        config.read("./fs_config.cfg")

        try:
            file_paths = config["folderpaths"]["paths"].split("\n")
            file_paths = filter_list(file_paths)

            # get all the files from the directories
            files = get_files(file_paths)

            # indexes all the files and categorises them
            index_data = prepare_index_data(files)

            # make the index file
            make_json_file(index_data)

        except KeyError:
            print(f"{Fore.RED}Important keys are missing !!")
            
            return False
        # print(config.sections())
    return True