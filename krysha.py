import json
import bs4
import requests
from datetime import date


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


def get_html(url: str):
    """ Получение кода страницы и преобразование его в html"""
    s = requests.Session()
    response = s.get(url=url, headers=headers)
    return response.text


def write_html_in_file(html: str):
    """
    Записывает данные странницы html в файл
    :param html: странца
    :return: Записывает данные html в index.html
    """
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(html)


def get_pages(html: str) -> int:
    """Получение количества страниц"""
    soup = bs4.BeautifulSoup(html, 'html')
    divs = soup.find('nav', class_='paginator')
    pages = divs.find_all('a', class_='paginator__btn')[-2].get('href')
    total_pages = pages.split('page=')[1].split('&')[0]
    return int(total_pages)


def get_data(html: str, date):
    """
    Ищет данные на одной странице
    """
    soup = bs4.BeautifulSoup(html, 'html')
    divs = soup.find('section', class_='a-list a-search-list a-list-with-favs')
    ads = divs.find_all('div', class_='a-card__inc')
    result_data = []
    for ad in ads:
        try:
            a = ad.find('a', class_='a-action a-action-favorite is-not-favorited')
            id = int(a.get('data-a-id'))
            print(id)
        except:
            id = ''
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
            div = ad.find('div', class_='card-stats').text.strip()
            release = ' '.join(div.split()[1:])
        except:
            release = ''
        try:
            div = ad.find('div', class_='a-card__header-left')
            url = "https://krisha.kz" + div.find('a').get('href')
        except:
            url = ''


        data = {'id': id,
                'title': kv,
                'price': price,
                'etaj': etaj,
                'square': square,
                'address': address,
                'description': descr,
                'url': url,
                'release': release
                }
        if date in release:
            result_data.append(data)
    return result_data


def collect_data(total_pages: int, url: str, date):
    """
    Перебирает все страницы и применяет функцию get_data(data). Записывает данные в json
    """
    s = requests.Session()
    result_all = []
    for i in range(1, total_pages + 1):
        pages = f'&page={i}'
        url = url + pages
        response = s.get(url=url, headers=headers)
        data = response.text
        result_temp = get_data(data, date)
        result_all.append(result_temp)

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_all, file, indent=4, ensure_ascii=False)

def main():
    price_from = 150000
    price_to = 200000
    current_date = str(date.today())[-2:]
    room = '2'
    cities = 'almaty'
    url = f"https://krisha.kz/arenda/kvartiry/{cities}/?das[_sys.hasphoto]=1&das[live.rooms][]={room}&das[price][from]={price_from}&das[price][to]={price_to}&das[rent.period]=2&das[who]=1"
    html = get_html(url=url)
    # write_html_in_file(html)
    total_pages = get_pages(html)
    collect_data(total_pages, url, current_date)
    get_data(html, current_date)


if __name__ == '__main__':
    main()
