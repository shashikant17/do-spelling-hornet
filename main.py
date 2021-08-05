from csv import writer

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

        unknown_words = unknown_words.union(
            unknowns
        )

    return unknown_words


def get_urls_for_checking() -> list:
    sitemap_listing = untangle.parse("https://www.dailyobjects.com/sitemap_important.xml")
    total_listing_urls = len(sitemap_listing.urlset.url)
    # sitemap_products_others = untangle.parse("https://www.dailyobjects.com/sitemap_products_others.xml")
    # urls.append([sitemap_products_others.urlset.url[index].loc.cdata for index in range(0, total_listing_urls)])
    return [sitemap_listing.urlset.url[index].loc.cdata for index in range(0, total_listing_urls)]


def write_results_to_csv(result: list) -> None:
    with open('misspelled_words.csv', 'w', newline='') as csv:
        file = writer(csv)
        file.writerows(result)


def main():
    result = [["url", "misspelled*"]]
    urls = get_urls_for_checking()
    print('Spell Checking {0} urls'.format(len(urls)))
    current_url_index = 0
    for url in urls:
        words = find_unknown_words(url)
        unknowns = " ".join(list(words))
        result.append([url, unknowns])
        current_url_index += 1
        print('Check for #{0} {1} : {2}'.format(current_url_index, url, unknowns))
        if current_url_index > 5:
            break
    write_results_to_csv(result)


if __name__ == '__main__':
    main()
