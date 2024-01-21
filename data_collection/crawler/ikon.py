from crawler.base import Base
import pandas as pd


class Ikon(Base):
    def __init__(self, url):
        super().__init__(url)

    def extract_data(self, soup):
        navbar = soup.find("div", class_="inavbar")
        if navbar:
            ul = navbar.find("ul")
            if ul:
                li = ul.find_all("li")
                if li:
                    for i in li:
                        if i.find("a"):
                            print(i.find("a").text)
