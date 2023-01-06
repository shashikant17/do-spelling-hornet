import requests
from bs4 import BeautifulSoup

import datetime

now = datetime.datetime.now()
todayDate = now.strftime("%d")
todayDateIndex = int(todayDate) % 10 # get index value of date

IGNORE_CHARS = ['\n', ',', '*', '?', '!', '.', '/', '-', ';', ':', '+', '(', ')']


class WebScraper:

    googleSmartPhone = {
            "User-Agent": "Mozilla/5.0 (Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/W.X.Y.Z‡ Mobile Safari/537.36 (compatible; "
                          "Googlebot/2.1; +http://www.google.com/bot.html)".encode('utf-8')
    }

    googleDesktop = {
            "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36".encode('utf-8')
    }

    def __init__(self):
        self.session = requests.session()
        self.headers = self.googleSmartPhone
        

        if todayDateIndex == 3 or 7:
            self.headers = self.googleDesktop


        """self.headers = {
            "User-Agent": "Mozilla/5.0 (Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/W.X.Y.Z‡ Mobile Safari/537.36 (compatible; "
                          "Googlebot/2.1; +http://www.google.com/bot.html)".encode('utf-8')
        }"""



    def scrape(self, url: str) -> list:
        response = self.session.get(
            url, headers=self.headers, allow_redirects=False
        )
        soup = BeautifulSoup(response.text.strip(), 'html.parser')
        # noinspection PyArgumentList

        html_text = soup.get_text(separator='|', strip=True)
        for ch in IGNORE_CHARS:
            html_text = html_text.replace(ch, " ")

        return html_text.split("|")
