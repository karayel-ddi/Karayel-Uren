from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class EksiSozlukScraper:
    def __init__(self, topic, max_pages=220):
        self.topic = topic
        self.max_pages = max_pages
        self.is_running = True
        self.base_url = f"https://eksisozluk.com/{self.topic}?p="

    def scrape(self):
        browser = webdriver.Firefox()
        page_count = 1

        while page_count <= self.max_pages and self.is_running:
            url = self.base_url + str(page_count)
            browser.get(url)

            elements = browser.find_elements(By.CSS_SELECTOR, ".content")
            for element in elements:
                yield [element.text]

            time.sleep(6)
            page_count += 1

        browser.close()