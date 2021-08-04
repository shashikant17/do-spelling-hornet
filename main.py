from pprint import pprint

from src.spell_checker import SpellChecker
from src.web_scraper import WebScraper


def find_unknown_words(url):
    scraper = WebScraper()
    page_texts = scraper.scrape(url)
    checker = SpellChecker()
    unknown_words = set()
    for page_text in page_texts:
        unknown_words.add(
            frozenset(
                checker.find_errors(
                    page_text.replace(".", " ").replace("\n", " ").replace(",", " ")
                )
            )
        )
    return unknown_words


if __name__ == '__main__':
    words = find_unknown_words('https://www.dailyobjects.com/')
    pprint(words)
