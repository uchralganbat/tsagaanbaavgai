from .base import Base
import pandas as pd
import logging
import os
import datetime
from src.common.models.article import Article
from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import Optional
from tqdm import tqdm


class Ikon(Base):
    def __init__(self, base_url):
        super().__init__(base_url)

        self.category = {
            "politics": "l/1",
            "economics": "l/2",
            "society": "l/3",
            "health": "l/16",
            "international": "l/4",
            "technology": "l/7",
        }

    def extract_data(self, output_filepath: str) -> None:
        next_url = self.category["politics"]

        date = datetime.datetime.now().strftime("%Y-%m-%d-%H")

        while next_url:
            soup = self.request_and_parse(path=next_url)
            next_url = self.get_next_page_url(soup)

            df = self.extract_articles(soup)

            with open(os.path.join(output_filepath, f"ikon-{date}.csv"), "a") as file:
                df.to_csv(file, index=False, header=False)
            logging.info(f"Extracted data from pagination: {next_url}")

        logging.info(f"Extracted data from all pagination")
        return

    def extract_articles(self, soup: BeautifulSoup) -> pd.DataFrame:
        pages = soup.find_all("div", {"class": "ikp_item"})
        articles = []

        for page in tqdm(pages, desc="Extracting from pages"):
            page_soup = self.request_and_parse(path=page.get("data-url"))
            items = page_soup.find_all("div", {"class": "nlitem"})
            for item in tqdm(items, desc="Extracting items", leave=False):
                article = self.extract_item(item=item)
                if article is not None:
                    articles.append(self.extract_item(item=item))

        return pd.DataFrame([article.__dict__ for article in articles])

    def extract_item(self, item: Tag) -> Optional[Article]:
        try:
            article_url = item.find("a").get("href")
            soup = self.request_and_parse(article_url)

            date = item.find("div", {"class": "nldate"}).get("rawdate")
            headline = item.find("div", {"class": "nlheadline"}).text.strip()
            title = item.find("div", {"class": "nlheader"}).text.strip()

            if "opinion" in article_url:
                core = soup.find("div", class_=["lrcore", "ikon-opinion"])
                author = core.find("a", {"class": "op_name"}).text
                content = (
                    core.find("div", {"class": "op_left_content"})
                    .findChild()
                    .get_text(strip=True, separator=" ")
                )

            else:
                content = soup.find("div", {"class": "inews"}).get_text(
                    strip=True, separator=" "
                )
                author = soup.find("div", {"class": "name"}).text.strip()

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

    def run_batch(self) -> Optional[list[Article]]:
        logging.info("Running batch")
        articles = []
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(
            "%m/%d/%Y %H:%M:%S"
        )

        for category in self.category.values():
            soup = self.request_and_parse(path=category)
            items = soup.find_all("div", {"class": "nlitem"})
            for item in items:
                if item.find("div", {"class": "nldate"}).get("rawdate") < yesterday:
                    article = self.extract_item(item=item)
                    if article is not None:
                        articles.append(article)

        return articles
