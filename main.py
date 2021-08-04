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
    current_url_index = 0
    while current_url_index < 2:
        current_url = sitemap_important.urlset.url[current_url_index].loc.cdata
        print('Checking {0} : {1}'.format(current_url_index, current_url))
        words = find_unknown_words(current_url)
        pprint(words)
        current_url_index += 1
