from crawler.ikon import Ikon

# List of URLs to scrape
urls_to_scrape = [
    "https://ikon.mn",
    "https://news.mn",
    "https://www.bloombergtv.mn/",
    "https://mongoltv.mn/news",
]

ikon = "https://ikon.mn"

if __name__ == "__main__":
    crawler = Ikon(ikon)
    crawler.crawl()
