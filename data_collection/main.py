from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
)
from selenium import webdriver

from crawler.ikon import Ikon

from bs4 import BeautifulSoup

import pandas as pd
import time

# List of URLs to scrape
urls_to_scrape = [
    "https://ikon.mn",
    "https://news.mn",
    "https://www.bloombergtv.mn/",
    "https://mongoltv.mn/news",
    "https://ergelt.mn",
]

ikon = "https://ikon.mn"

if __name__ == "__main__":
    """
    Politic articles
    """

    ikon_instance = Ikon(ikon)
    df = ikon_instance.extract_data()

    df.to_csv("politics.csv", index=False, mode="w")
