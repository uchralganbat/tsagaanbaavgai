import requests
from bs4 import BeautifulSoup


class Base:
    def __init__(self, url):
        self.url = url

    def make_request(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error making request to {self.url}: {e}")

    def parse_html(self, html_content):
        return BeautifulSoup(html_content, "html.parser")

    def crawl(self):
        html_content = self.make_request()
        soup = self.parse_html(html_content)
        self.extract_data(soup)

    def extract_data(self, soup):
        raise NotImplementedError("Subclasses must implement the extract_data method.")
