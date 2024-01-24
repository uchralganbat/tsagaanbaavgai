from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException as StaleElement
from selenium import webdriver

import bs4 as bs

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
    category = {
        "politics": "l/1",
        "economics": "l/2",
    }

    driver = webdriver.Chrome()
    driver.get(f"{ikon}/l/1")

    """
        Politic articles
    """

    try:
        data = {
            "date": [],
            "headline": [],
            "url": [],
            "main": [],
            "author": [],
            "article_source": [],
            "title": [],
        }
        pagination = driver.find_element(by=By.CLASS_NAME, value="ikpagination")

        wait = WebDriverWait(driver, timeout=2)
        wait.until(lambda d: pagination.is_displayed())

        pages = driver.find_elements(by=By.CLASS_NAME, value="ikp_item")

        for page in pages:
            try:
                page_url = page.get_attribute("data-url")

                driver.get(f"{ikon}{page_url}")

                news_list_container = WebDriverWait(driver, timeout=2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "newslistcontainer"))
                )

                items = news_list_container.find_elements(
                    by=By.CLASS_NAME, value="nlitem"
                )

                for item in items:
                    date = item.find_element(
                        by=By.CLASS_NAME, value="nldate"
                    ).get_attribute("rawdate")

                    headline = item.find_element(
                        by=By.CLASS_NAME, value="nlheadline"
                    ).text

                    url = item.find_element(By.TAG_NAME, "a").get_attribute("href")

                    print(date, headline, url)

                    driver.get(url)

                    news = driver.find_element(by=By.CLASS_NAME, value="inews")

                    title = news.find_element(by=By.TAG_NAME, value="h1").text

                    author = news.find_element(by=By.CLASS_NAME, value="name").text
                    main = " ".join(
                        [p.text for p in news.find_elements(By.TAG_NAME, "p")]
                    )
                    article_source = news.find_element(By.TAG_NAME, "strong").text

                    data["article_source"].append(article_source)
                    data["author"].append(author)
                    data["main"].append(main)
                    data["title"].append(title)
                    data["url"].append(url)
                    data["date"].append(date)
                    data["headline"].append(headline)

                    driver.back()

            except StaleElement:
                print("Element is stale. Skipping")

    finally:
        driver.quit()

    df = pd.DataFrame(data)

    df.to_csv("politics.csv", index=False)
