import json
import os
import re
from configparser import ConfigParser
from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


@dataclass
@dataclass_json
class Institution:
    elsevier_id: str
    name: str
    uri: str
    country: str
    country_code: str
    rank: int = None


def get_secret(name: str, file="config.ini"):
    config = ConfigParser()
    config.read(file)
    return config["SECRETS"][name]


def load_institutions() -> List[Institution]:
    files = os.listdir("Data/Scival")
    files = [x for x in files if x.endswith("json")]
    files.sort(key=lambda x: int(x.split("_")[0]))
    institutions = []
    for item in files:
        with open(f"Data/Scival/{item}", "r") as file:
            dic = json.load(file)
        # print(f"{dic['elsevier_id']} - {dic['name']}")
        institution = Institution(dic['elsevier_id'], dic['name'], None, None, None, rank=int(item.split("_")[0]))
        institutions.append(institution)
    return institutions


def isnumber(x):
    try:
        float(x)
        return True
    except:
        return False


def camel_case_to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
