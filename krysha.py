import json
import pprint

import bs4
import requests

import requests
from time import sleep
from selenium import webdriver
import urllib.request

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


def get_html(url: str):
    """ получение кода страницы """
    s = requests.Session()
    response = s.get(url=url, headers=headers)
    return response.text


def write_html_in_file(html: str):
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(html)


def get_pages(html: str) -> int:
    """Получение количества страниц"""
    soup = bs4.BeautifulSoup(html, 'html')
    divs = soup.find('nav', class_='paginator')
    pages = divs.find_all('a', class_='paginator__btn')[-2].get('href')
    total_pages = pages.split('page=')[1].split('&')[0]
    return int(total_pages)


def get_data(html: str):
    """Ищет нужные данные на странице"""
    soup = bs4.BeautifulSoup(html, 'html')
    divs = soup.find('section', class_='a-list a-search-list a-list-with-favs')
    ads = divs.find_all('div', class_='a-card__inc')
    # pages = str(divs.find_all('a', class_='a-card__title'))
    # data_name = [i.strip('</a') for i in pages.split('>')[1::2]]
    result_data = []
    for ad in ads:
        try:
            div = ad.find('a', class_='a-card__title').text
            kv = div.split(",")[0]
        except:
            kv = ''
        try:
            div = ad.find('a', class_='a-card__title').text
            square = div.split(",")[1]
        except:
            square = ''
        try:
            div = ad.find('a', class_='a-card__title').text
            etaj = div.split(",")[2]
        except:
            etaj = ''

        try:
            price = ad.find('div', class_='a-card__price').text.strip()
        except:
            price = ''
        try:
            address = ad.find('div', class_='a-card__subtitle').text.strip()
        except:
            address = ''
        try:
            descr = ad.find('div', class_='a-card__text-preview').text.strip()
        except:
            descr = ''
        try:
            start = ad.find('span', class_='a-view-count status-item').text.strip()
        except:
            start = ''
        try:
            div = ad.find('div', class_='a-card__header-left')
            url = "https://krisha.kz" + div.find('a').get('href')
            # tel = ''
        except:
            url = ''
            # tel = ''

        data = {'title': kv,
                'price': price,
                'etaj': etaj,
                'square': square,
                'address': address,
                'description': descr,
                'url': url,
                'start': start
                }
        result_data.append(data)
    return result_data


def collect_data(total_pages: int, url):
    s = requests.Session()
    result_all = []
    for i in range(1, total_pages + 1):
        pages = f'&page={i}'
        url = url + pages
        response = s.get(url=url, headers=headers)
        data = response.text
        result_temp = get_data(data)
        result_all.append(result_temp)
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_all, file, indent=4, ensure_ascii=False)

def main():

    price_from = 150000
    price_to = 200000
    url = f"https://krisha.kz/arenda/kvartiry/almaty/?das[_sys.hasphoto]=1&das[live.rooms][]=1&das[live.rooms][]=2&das[price][from]={price_from}&das[price][to]={price_to}&das[rent.period]=2&das[who]=1"
    html = get_html(url=url)
    # write_html_in_file(html)
    total_pages = get_pages(html)
    collect_data(total_pages, url)
    get_data(html)
if __name__ == '__main__':
    main()
