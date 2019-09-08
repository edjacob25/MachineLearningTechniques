import configparser
import os
from dataclasses import dataclass
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException


@dataclass
class Identity:
    username: str
    last_name: str
    pin: str


def download_org_data(org: str, identity: Identity):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    dir_path = os.getcwd()
    profile.set_preference("browser.download.dir", f"{dir_path}/Data")
    profile.set_preference("browser.download.folderList", 2)

    browser = webdriver.Firefox(firefox_profile=profile)
    try:
        browser.get("http://0-www.scopus.com.millenium.itesm.mx/home.url")
        browser.find_element_by_name("name").send_keys(identity.last_name)
        browser.find_element_by_name("code").send_keys(identity.username)
        browser.find_element_by_name("pin").send_keys(identity.pin)
        browser.find_element_by_name("submit").click()
        try:
            browser.find_element_by_id("affilSearchLink").click()
            browser.find_element_by_id("affilName").send_keys(org)
            browser.find_element_by_id("affilSearch").click()
        except ElementClickInterceptedException:
            browser.find_element_by_xpath("//a[@pendo-id='Continue as guest']").click()
            browser.find_element_by_id("affilSearchLink").click()
            browser.find_element_by_id("affilName").clear()
            browser.find_element_by_id("affilName").send_keys(org)
            browser.find_element_by_id("affilSearch").click()

        browser.find_element_by_class_name("docTitle").click()
        browser.find_element_by_id("export_results").click()
        browser.find_element_by_class_name("exportButton").click()
    finally:
        browser.close()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")
    identity = Identity(config["IDENTITY"]["username"], config["IDENTITY"]["last_name"], config["IDENTITY"]["pin"])
    filename = "Data/2019-QS-World-University-Rankings.txt"
    universities = []
    with open(filename, "r") as file:
        for line in file:
            universities.append(line.split(", ")[-1].strip())

    for univ in universities:
        pass
        # download_org_data(univ, identity)
    download_org_data("HARVARD UNIVERSITY", identity)
