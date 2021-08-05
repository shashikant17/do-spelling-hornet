from pprint import pprint

import untangle

from src.spell_checker import SpellChecker
from src.web_scraper import WebScraper


def find_unknown_words(url):
    scraper = WebScraper()
    page_texts = scraper.scrape(url)
    checker = SpellChecker()
    unknown_words = set()
    for page_text in page_texts:
        if len(page_text) == 0 or page_text.find('\'') >= 0 \
                or page_text.find('’') >= 0 or page_text.find('”') >= 0:
            continue

        unknowns = frozenset(checker.find_errors(page_text))

        if len(unknowns) == 0:
            continue

        unknown_words.add(
            unknowns
        )

    return unknown_words


if __name__ == '__main__':
    sitemap_important = untangle.parse("https://www.dailyobjects.com/sitemap_important.xml")
    total_urls = len(sitemap_important.urlset.url)
    print('Spell Checking {0} urls'.format(total_urls))
    urls = [sitemap_important.urlset.url[index].loc.cdata for index in range(0, total_urls)]
    urls = [
        "https://www.dailyobjects.com/dailyobjects-binge-watch-stride-clear-case-cover-for-iphone-12/dp?f=pid~STRD-CLR-BING-WATC-DOB-AP-IPH12"]
    current_url_index = 0
    for url in urls:
        print('Checking {0} : {1}'.format(current_url_index, url))
        words = find_unknown_words(url)
        pprint(words)
        current_url_index += 1
        break
