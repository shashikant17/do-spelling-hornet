import sys
import time
import datetime
from csv import writer

import untangle

from src.spell_checker import SpellChecker
from src.web_scraper import WebScraper

# Get date of the month
now = datetime.datetime.now()
print(now.strftime("%A"))
day = now.strftime("%A")

# todays date
todayDate = now.strftime("%d")

# is_odd function is for checking date is even or not
def is_odd(num):
    if num % 2 == 0:
        return False
    else:
        return True

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


def get_urls_for_checking(sitemap: str) -> list:
    sitemap_listing = untangle.parse(sitemap)
    total_listing_urls = len(sitemap_listing.urlset.url)
    return [sitemap_listing.urlset.url[index].loc.cdata for index in range(0, total_listing_urls)]


def write_results_to_csv(result: list) -> None:
    with open('misspelled_words.csv', 'w', newline='') as csv:
        file = writer(csv)
        file.writerows(result)


def main():
    result = [["url", "misspelled*"]]
    urls = []

    """urls = ["sitemap_important.xml",
            "sitemap_other.xml",
            "sitemap_other_products.xml",
            "sitemap_apple_cases_products.xml",
            "sitemap_android_oneplue_cases_products.xml",
            "sitemap_android_samsung_cases_products.xml",
            "sitemap_android_other_cases_products.xml"]
    """

    # runs on odd dates like 1,3,5,7,9
    oddURL = [
        "sitemap_important.xml",
        "sitemap_other.xml",
    ]

    # runs on even dates like 2, 4, 6, 8, 10
    evenURL = {
        "0": "sitemap_other_products.xml",
        "2": "sitemap_apple_cases_products.xml",
        "4": "sitemap_android_other_cases_products.xml",
        "6": "sitemap_android_oneplue_cases_products.xml",
        "8": "sitemap_android_samsung_cases_products.xml"
    }

    """
    mtURL = ["sitemap_important.xml",
            "sitemap_other.xml",
            "sitemap_other_products.xml"
    ]

    wtURl = [
        "sitemap_apple_cases_products.xml",
        "sitemap_android_oneplue_cases_products.xml",
    ]

    fsURL = [
            "sitemap_android_samsung_cases_products.xml",
            "sitemap_android_other_cases_products.xml"
    ]
    """
            
    todayURL = []
    
    global todayDateIndex # global variable because we've to use it in web_scraper.py
    todayDateIndex = int(todayDate) % 10 # get index value of date

    if is_odd(todayDateIndex):
        todayURL = oddURL
    elif(todayDateIndex == 0):
        todayURL = evenURL.get("0")
    elif(todayDateIndex == 2):
        todayURL = evenURL.get("2")
    elif(todayDateIndex == 4):
        todayURL = evenURL.get("4")
    elif(todayDateIndex == 6):
        todayURL = evenURL.get("6")
    elif(todayDateIndex == 8):
        todayURL = evenURL.get("8")


    print(todayURL)

    """
    if day == "Monday":
        print(day)
        todayURL = mtURL
    elif day == "Tuesday":
        print(day)
        todayURL = mtURL
    elif day == "Wednesday":
        print(day)
        todayURL = wtURl
    elif day == "Thursday":
        print(day)
        todayURL = wtURl
    elif day == "Friday":
        print(day)
        todayURL = fsURL
    elif day == "Saturday":
        print(day)
        todayURL = fsURL
    """

    # for i in range(1, len(sys.argv)):
    #     urls.extend(get_urls_for_checking('https://www.dailyobjects.com/{0}'.format(sys.argv[i])))

    for i in range(0, len(todayURL)):
        urls.extend(get_urls_for_checking('https://www.dailyobjects.com/{0}'.format(todayURL[i])))
    
    print('Spell Checking {0} urls'.format(len(urls)))
    current_url_index = 0

    for url in urls:
        try:
            start_time = time.time()
            words = find_unknown_words(url)
            unknowns = " ".join(list(words))
            result.append([url, unknowns])
            current_url_index += 1
            print(
                'Check for #{0} {1} : {2} in {3}ms'.format(current_url_index, url.split(".com")[1],
                                                           unknowns,
                                                           round((time.time() - start_time) * 1000),
                                                           2))
        except ConnectionError:
            print('Error Checking for #{0} {1}'.format(current_url_index, url))
    write_results_to_csv(result)


if __name__ == '__main__':
    main()
