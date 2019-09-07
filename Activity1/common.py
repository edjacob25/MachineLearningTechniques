import json
import os
from configparser import ConfigParser
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List


@dataclass
@dataclass_json
class Institution:
    elsevier_id: str
    name: str
    uri: str
    country: str
    country_code: str


def get_secret(name: str, file="config.ini"):
    config = ConfigParser()
    config.read(file)
    return config["SECRETS"][str]


def load_institutions() -> List[Institution]:
    for item in os.listdir("Data/Scival"):
        dic = json.load(item)
        print(f"{dic['elsevier_id']} - {dic['name']}")
    return []
