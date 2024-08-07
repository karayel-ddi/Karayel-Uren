import requests
import time
from bs4 import BeautifulSoup

class SikayetvarScraper:
    def __init__(self, brand):
        self.brand = brand
        self.base_url = 'https://www.sikayetvar.com/'
        self.is_running = True
        self.start_page = 1  # Başlangıç sayfası
        self.end_page = 350  # Bitiş sayfası
    
    def marka_sayfasi(self, sayfa):
        url = f'{self.base_url}{self.brand}?page={sayfa}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            return False

    def sikayet_sayfasi(self, link):
        url = f'{self.base_url}{link}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            return False

    def scrape(self):
        page = self.start_page
        while self.is_running and page <= self.end_page:
            soup = self.marka_sayfasi(page)
            if not soup:
                break

            sikayet_linkler = [l['href'] for l in soup.find_all('a', class_='complaint-layer') if l['href'].count(self.brand) > 0]
            for link in sikayet_linkler:
                if not self.is_running:
                    break
                soup_sikayet = self.sikayet_sayfasi(link)
                if not soup_sikayet or soup_sikayet.find('div', class_="complaint-detail-description") is None:
                    continue
                text = ""
                for k in soup_sikayet.find('div', class_="complaint-detail-description").text.split(" ")[1:]:
                    text += k + " "
                yield [text.strip()]
            page += 1
            time.sleep(3)
