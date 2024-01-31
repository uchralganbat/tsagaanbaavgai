import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class Base:
    def __init__(self, base_url):
        self.base_url = base_url
        self.driver = webdriver.Chrome()

    def request_and_parse(self, path: str) -> BeautifulSoup:
        url = "{}/{}".format(self.base_url, path)
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error making request to {url}: {e}")

    def extract_data(self):
        raise NotImplementedError("Subclasses must implement the extract_data method.")
