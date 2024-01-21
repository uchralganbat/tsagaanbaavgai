from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver


import pandas as pd


# List of URLs to scrape
urls_to_scrape = [
    "https://ikon.mn",
    "https://news.mn",
    "https://www.bloombergtv.mn/",
    "https://mongoltv.mn/news",
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
        pagination = driver.find_element(by=By.CLASS_NAME, value="ikpagination")

        wait = WebDriverWait(driver, timeout=2)
        wait.until(lambda d: pagination.is_displayed())

        pages = driver.find_elements(by=By.CLASS_NAME, value="ikp_item")

        for page in pages:
            page.click()

            wait.until(
                lambda d: d.find_element(by=By.CLASS_NAME, value="newslistcontainer")
            )

            news = page.find_elements(by=By.CLASS_NAME, value="nlitem")

            for item in news:
                date = item.find_element(
                    by=By.CLASS_NAME, value="nldate"
                ).get_attribute("rawdate")

                headline = item.find_element(by=By.CLASS_NAME, value="nlheadline").text

                title, url = item.find_element(
                    By.TAG_NAME, "a"
                ).text, item.find_element(By.TAG_NAME, "a").get_attribute("href")

                print(date, headline, title, url)

    finally:
        driver.quit()
