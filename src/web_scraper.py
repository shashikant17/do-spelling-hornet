import requests
from bs4 import BeautifulSoup

IGNORE_CHARS = ['\n', ',', '*', '?', '!', '.', '/', '-', ';', ':', '+', '(', ')']


class WebScraper:
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/W.X.Y.Z‡ Mobile Safari/537.36 (compatible; "
                          "Googlebot/2.1; +http://www.google.com/bot.html)".encode('utf-8')
        }

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
