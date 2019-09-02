import configparser
import json
import requests
from dataclasses import dataclass
from itertools import zip_longest
from time import sleep
from typing import List


@dataclass
class Institution:
    elsevier_id: str
    name: str
    uri: str
    country: str
    country_code: str


def authorize(apikey: str) -> str:
    url = "http://api.elsevier.com/authenticate?platform=SCOPUS"
    headers = {"X-ELS-APIKey": apikey, "Accept": "application/json"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print(r.json())
        return r.json()["authenticate-response"]["authtoken"]
    else:
        raise Exception("authorization error")


def search(apikey: str, token: str):
    url = "https://api.elsevier.com/content/search/scopus"
    headers = {"X-ELS-APIKey": apikey, "Accept": "application/json"}
    payload = {"query": "ALL(MIT)"}
    r = requests.get(url, headers=headers, params=payload)
    print(r.status_code)
    results = r.json()["search-results"]
    print(len(results["entry"]))
    print(r.json())


def institution_search(apikey: str, inst: str, token: str) -> List[Institution]:
    url = " https://api.elsevier.com/metrics/institution/search"
    headers = {"X-ELS-APIKey": apikey, "Accept": "application/json"}
    payload = {"query": f"name({inst})"}
    r = requests.get(url, headers=headers, params=payload)
    print(r.status_code)
    print(r.json())
    options = []
    for result in r.json()["results"]:
        institution = Institution(result["id"], result["name"], result["uri"], result["country"], result["countryCode"])
        options.append(institution)
    return options


def get_scival_info(apikey: str, elsevier_id: str):
    print(elsevier_id)
    url = "https://api.elsevier.com/analytics/scival/institution/metrics"
    headers = {"X-ELS-APIKey": apikey, "Accept": "application/json"}

    metrics = ["ScholarlyOutput", "CitedPublications", "AcademicCorporateCollaboration",
               "AcademicCorporateCollaborationImpact", "Collaboration", "CitationCount", "CitationsPerPublication",
               "CollaborationImpact", "FieldWeightedCitationImpact", "PublicationsInTopJournalPercentiles",
               "OutputsInTopCitationPercentiles"]

    with open(f"Data/request_{elsevier_id}.json", "w") as file:
        params = {"metricTypes": ",".join(metrics), "institutionIds": elsevier_id, "yearRange": "10yrs",
                  "includeSelfCitations": "true", "byYear": "true", "includedDocs": "AllPublicationTypes",
                  "journalImpactType": "CiteScore", "showAsFieldWeighted": "false", "indexType": "hIndex"}
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == 200:
            print(r.status_code)
            print(r.text)
            result = r.json()["results"][0]["metrics"]
            file.write(json.dumps(result))
        sleep(1)
    return result


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")

    apikey = config["SECRETS"]["elsevier_apikey"]
    try:
        token = config["SECRETS"]["elsevier_authtoken"]
        print("Auth")
    except KeyError:
        token = authorize(apikey)
        print(token)

    filename = "Data/2019-QS-World-University-Rankings.txt"
    with open(filename, "r") as file:
        for line in file:
            uni = line.split(", ")[-1].strip()
            try:
                possible_institutions = institution_search(apikey, uni, token)
                data = get_scival_info(apikey, possible_institutions[0].elsevier_id)
            except IndexError:
                print(f"University {uni} could not be found")

    #possible_institutions = institution_search(apikey, "Harvard University", token)
    #data = get_scival_info(apikey, possible_institutions[0].elsevier_id)