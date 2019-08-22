import configparser
from elsapy import elsclient
from elsapy.elssearch import ElsSearch

base_url = ""

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")

    client = elsclient.ElsClient(config["KEYS"]["elsevier_apikey"])

    aff_srch = ElsSearch('affil(amsterdam)', 'affiliation')
    aff_srch.execute(client)
    print("aff_srch has", len(aff_srch.results), "results.")
