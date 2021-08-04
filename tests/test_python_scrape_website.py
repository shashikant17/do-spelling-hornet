import unittest

from src.web_scraper import WebScraper


class WebScrapTestCase(unittest.TestCase):
    def test_scraping(self):
        scraper = WebScraper()
        page_text = scraper.scrape('https://www.dailyobjects.com')
        self.assertIsNotNone(page_text)


if __name__ == '__main__':
    unittest.main()
