from websites.base import Base
import pandas as pd
import logging
import os
from dataclasses import dataclass
from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import Optional


@dataclass
class Article:
    date: str
    headline: str
    url: str
    content: str
    author: str
    title: str
    category: str
    source: str


class Ikon(Base):
    def __init__(self, base_url):
        super().__init__(base_url)

        self.category = {
            "politics": "l/1",
            "economics": "l/2",
        }

    def extract_data(self, output_filepath: str, date: str) -> None:
        next_url = self.category["politics"]

        while next_url:
            soup = self.request_and_parse(path=next_url)
            next_url = self.get_next_page_url(soup)
            df = self.extract_articles(soup)

            with open(os.path.join(output_filepath, f"ikon-{date}.csv"), "a") as file:
                df.to_csv(file, index=False)
            logging.info(f"Extracted data from pagination: {next_url}")

        logging.info(f"Extracted data from all pagination")
        return

    def extract_articles(self, soup: BeautifulSoup) -> pd.DataFrame:
        pages = soup.find_all("div", {"class": "ikp_item"})
        articles = []

        for page in pages:
            page_soup = self.request_and_parse(path=page.get("data-url"))
            items = page_soup.find_all("div", {"class": "nlitem"})
            for item in items:
                article = self.extract_item(item=item)
                if article is not None:
                    articles.append(self.extract_item(item=item))
            logging.info(f"Extracted data from page: {page.get('data-url')}")

        return pd.DataFrame([article.__dict__ for article in articles])

    def extract_item(self, item: Tag) -> Optional[Article]:
        try:
            article_url = item.find("a").get("href")
            if "opinion" in article_url:
                print("opinion article")
                return

            date = item.find("div", {"class": "nldate"}).get("rawdate")
            headline = item.find("div", {"class": "nlheadline"}).text.strip()
            title = item.find("div", {"class": "nlheader"}).text.strip()

            soup = self.request_and_parse(article_url)
            news = soup.find("div", {"class": "inews"})

            content = " ".join([p.text for p in news.find_all("p")])
            author = news.find("div", {"class": "name"}).text

            return Article(
                date=date,
                headline=headline,
                url=f"{self.base_url}/{article_url}",
                content=content,
                author=author,
                title=title,
                category="politics",
                source="ikon",
            )

        except Exception as e:
            logging.error(
                f"Error extracting data from item: {e}, \n article url: {article_url}"
            )

    def get_next_page_url(self, soup: BeautifulSoup) -> Optional[str]:
        next_page = soup.find("i", {"class": "ikon-right-dir"})
        if next_page:
            return next_page.get("data-url")
        else:
            logging.info("No next page URL found.")
            return None

    def run_batch(self):
        logging.info("Running batch")
