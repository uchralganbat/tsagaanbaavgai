from websites.base import Base
import pandas as pd


class Ikon(Base):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.data = {
            "date": [],
            "headline": [],
            "url": [],
            "main": [],
            "author": [],
            "title": [],
        }

        # self.df = pd.DataFrame(
        #     columns=["date", "headline", "url", "main", "author", "title"]
        # )

        self.category = {
            "politics": "l/1",
            "economics": "l/2",
        }

    def extract_data(self):
        soup = self.request_and_parse(self.category["politics"])

        pages = soup.find_all("div", {"class": "ikp_item"})

        for page in pages:
            page_soup = self.request_and_parse(page.get("data-url"))

            items = page_soup.find_all("div", {"class": "nlitem"})
            for item in items:
                self.extract_item(item)

        return pd.DataFrame(self.data, columns=self.data.keys())

    def extract_item(self, item):
        try:
            article_url = item.find("a").get("href")
            match article_url:
                case "opinion" if "opinion" in article_url:
                    print("opinion article")
                    return

                case _:
                    date = item.find("div", {"class": "nldate"}).get("rawdate")
                    headline = item.find("div", {"class": "nlheadline"}).text.strip()
                    title = item.find("div", {"class": "nlheader"}).text.strip()

                    soup = self.request_and_parse(article_url)
                    news = soup.find("div", {"class": "inews"})

                    main = " ".join([p.text for p in news.find_all("p")])
                    author = news.find("div", {"class": "name"}).text

                    # row = {
                    #     "date": date,
                    #     "headline": headline,
                    #     "url": f"{self.base_url}/{article_url}",
                    #     "main": main,
                    #     "author": author,
                    #     "title": title,
                    # }

        except Exception as e:
            print(e)
            print(article_url)
            return

        # self.df = self.df.append(row, ignore_index=True)
        self.data["date"].append(date)
        self.data["headline"].append(headline)
        self.data["url"].append(f"{self.base_url}/{article_url}")
        self.data["title"].append(title)
        self.data["main"].append(main)
        self.data["author"].append(author)
