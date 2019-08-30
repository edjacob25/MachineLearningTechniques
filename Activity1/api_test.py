import configparser
import json
import requests


def authorize(apikey: str) -> str:
    url = "http://api.elsevier.com/authenticate?platform=SCOPUS"
    headers = {"X-ELS-APIKey": apikey, "Accept": "application/json"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()["authtoken"]
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


def institution_search(apikey: str, inst: str, token: str):
    url = " https://api.elsevier.com/metrics/institution/search"
    headers = {"X-ELS-APIKey": apikey, "Accept": "application/json"}
    payload = {"query": f"name({inst})"}
    r = requests.get(url, headers=headers, params=payload)
    print(r.status_code)
    print(r.json())


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")

    apikey = config["SECRETS"]["elsevier_apikey"]
    token = config["SECRETS"]["elsevier_authtoken"]
    if not token:
        print("Auth")
        token = authorize(apikey)
    institution_search(apikey, "Harvard University", token)
    # search(apikey, token)