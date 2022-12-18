import json
import os


def json2list(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    for key, value in data.items():
        value["name"] = key
    return list(data.values())


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
