import configparser
import json
import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from itertools import zip_longest
from time import sleep
from typing import List


@dataclass
@dataclass_json
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
    

def institution_search(apikey: str, inst: str, token: str) -> List[Institution]:
    url = "https://api.elsevier.com/metrics/institution/search"
    headers = {"X-ELS-APIKey": apikey, "Accept": "application/json"}
    payload = {"query": f"name({inst})"}
    r = requests.get(url, headers=headers, params=payload)
    options = []
    for result in r.json()["results"]:
        institution = Institution(result["id"], result["name"], result["uri"], result["country"], result["countryCode"])
        options.append(institution)
    return options

def institution_group_search(apikey: str, inst: str, token: str) -> List[Institution]:
    url = "https://api.elsevier.com/analytics/scival/institutionGroup/search"
    headers = {"X-ELS-APIKey": apikey, "Accept": "application/json"}
    payload = {"query": f"name({inst})"}
    r = requests.get(url, headers=headers, params=payload)
    options = []
    for result in r.json()["results"]:
        institution = Institution(result["id"], result["name"], result["uri"], None, None)
        options.append(institution)
    return options

def get_scival_info(apikey: str, inst: Institution, rank: int):
    print(inst.elsevier_id)
    url = "https://api.elsevier.com/analytics/scival/institution/metrics"
    headers = {"X-ELS-APIKey": apikey, "Accept": "application/json"}

    metrics = ["ScholarlyOutput", "CitedPublications", "AcademicCorporateCollaboration",
               "AcademicCorporateCollaborationImpact", "Collaboration", "CitationCount", "CitationsPerPublication",
               "CollaborationImpact", "FieldWeightedCitationImpact", "PublicationsInTopJournalPercentiles",
               "OutputsInTopCitationPercentiles"]

    with open(f"Data/Scival/{rank}_{inst.name}_{inst.elsevier_id}.json", "w") as file:
        params = {"metricTypes": ",".join(metrics), "institutionIds": inst.elsevier_id, "yearRange": "10yrs",
                  "includeSelfCitations": "true", "byYear": "true", "includedDocs": "AllPublicationTypes",
                  "journalImpactType": "CiteScore", "showAsFieldWeighted": "false", "indexType": "hIndex"}
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == 200:
            print(r.status_code)
            result = r.json()["results"][0]["metrics"]
            entity = inst.to_dict()
            entity["metrics"] = result
            file.write(json.dumps(entity))
        sleep(1)
    return result

def decide(institutions: List[Institution]) -> int:
    for i, institution in enumerate(institutions):
        print(f"{i}: {institution.name}")
    res = input("Choose one: ")
    return res

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
        for rank, line in enumerate(file):
            rank = rank
            uni = line.split(", ")[-1].strip()
            uni = uni.replace("(", "")
            uni = uni.replace(")", "")
            try:
                possible_institutions = institution_search(apikey, uni, token)
                if len(possible_institutions) > 1:
                    print(f"To decide about: {uni}")
                    chosen = decide(possible_institutions)
                    if chosen == "s":
                        groups = institution_group_search(apikey, uni, token)
                        possible_institutions.extend(groups)
                        chosen = decide(possible_institutions)
                    if chosen == "a":
                        with open("Data/ToMerge.txt", "a+") as merge:
                            for inst in possible_institutions:
                                merge.write(f"{inst.elsevier_id}, {inst.name}, {inst.country}\n")
                            merge.write("\n")
                        continue
                    chosen = int(chosen)
                    print(f"{uni} -> {possible_institutions[chosen].name}")
                    data = get_scival_info(apikey, possible_institutions[chosen], rank)
                elif len(possible_institutions) == 0:
                    while (1):
                        print(f"Institution {uni} not found, change the text")
                        a = input("New text: ")
                        print(f"New text is {a}")
                        new_options = institution_search(apikey, a, token)
                        new_options.extend(institution_group_search(apikey, a, token))
                        #print(new_options)
                        chosen = int(decide(new_options))
                        if chosen == -1:
                            pass
                        elif chosen == -2:
                            break
                        else:
                            print(f"{uni} -> {new_options[chosen].name}")
                            data = get_scival_info(apikey, new_options[chosen], rank)
                            break

                else:
                    print(f"{uni} -> {possible_institutions[0].name}")
                    data = get_scival_info(apikey, possible_institutions[0], rank)
            except IndexError:
                with open("Data/NotFound.txt", "a+") as not_found:
                    not_found.write(f"{uni}\n")
                print(f"University {uni} could not be found")

    #possible_institutions = institution_search(apikey, "Harvard University", token)
    #data = get_scival_info(apikey, possible_institutions[0].elsevier_id)