# https://www.avito.ru/kaliningrad/noutbuki?cd=1&s=1&user=1
import sys
import requests, fake_useragent  # pip install requests
import json
import re
from bs4 import BeautifulSoup

class avito():
    """parsing avito.ru for Russia"""
    def __init__(self, url="https://www.avito.ru/kaliningrad/noutbuki?cd=1&s=1&user=1", filename="avito.json"):
        self.url = url
        self.filename = filename
        self.error = []

    @staticmethod
    def p(text, *args):
        print(text, *args, sep=' / ', end='\n')

    def write_json(self, data, path = None):
        path = self.filename if path is None else path
        with open(path, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_json(self, path = None):
        path = self.filename if path is None else path
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
        return {}  

    # Random User-Agent
    def get_html(self, url_page = None):
        ua = fake_useragent.UserAgent() 
        user = ua.random
        header = {'User-Agent':str(user)}
        url_page = self.url if url_page is None else url_page
        try:
            page = requests.get(url_page, headers = header, timeout = 10)
            return page.text
        except Exception as e:
            print(sys.exc_info()[1])
            return False
    
    def get_all_links(self, html):
        if html is False:
            return False
        soup = BeautifulSoup(html, 'lxml')
        selection_list = soup.find('div', {'data-marker':'catalog-serp'})    
        # self.p(soup.find('h1').text.strip())
        # self.p(selection_list)
        
        links = []
        if selection_list is not None:
            for r_ in selection_list.find_all('div', {'data-marker':'item'}):
                # add item ads
                try:
                    item_ = r_.find('a', {'data-marker':'item-title'})
                    item_a = item_.get('href')
                    item_name = item_.text.strip()
                    prise = r_.find('span', {'data-marker':'item-price'})
                    item_prise = prise.find('meta', {'itemprop':'price'}).get('content')
                    item_currency = prise.find('meta', {'itemprop':'priceCurrency'}).get('content')
                    item_date = r_.find('div', {'class':'date-root-QeIIB'}).text.strip()
                    item_description = r_.find('meta', {'itemprop':'description'}).get('content').strip()
                    item_adress = r_.find('div', {'class':'geo-root-H3eWU'}).text.strip()
                    user_ = r_.find('a', {'data-marker':'item-link'})
                    item_user = user_.text.strip()
                    right_ = r_.find('div', {'class':'iva-item-aside-c_vio'})
                    items_span = ", ".join([x.text.strip() for x in right_.find_all('span', {'class':'text-text-LurtD'})])
                    

                    row = []
                    row.append(item_a)
                    row.append(item_name)
                    row.append(item_prise)
                    row.append(item_currency)                
                    row.append(item_date)
                    row.append(item_adress)
                    row.append(item_description)
                    row.append(item_user)
                    row.append(items_span)
                    links.append(row)
                except Exception as e:
                    print(sys.exc_info()[1])
                    continue
        else:
            self.error.append(soup.find('h1').text.strip())
        
        return links