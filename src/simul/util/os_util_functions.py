# TODO DESCRIPTION AND COMMENTS

import os
import shutil


def init_folders(paths):
    for folder in paths:
        try:
            shutil.rmtree(folder)
        except OSError as e:
            pass
        os.mkdir(folder)


def search_for_files(path: str):
    files_list = []
    for root, dirs, files in os.walk(path):
        for name in files:
            files_list.append(os.path.join(root, name))
    return files_list


def search_a_path(path_name: str, paths: str) -> str:
    for path in paths:
        if path_name in path:
            return path


def correct_directory_path(path: str):
    if (path[len(path)-1] != "/"):
        path += "/"
    return path


def save_file(file: str, content: str, method: str):
    file = open(file, method)
    file.writelines(content)
    file.close()
