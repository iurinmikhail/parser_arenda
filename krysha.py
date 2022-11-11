import requests
from bs4 import BeautifulSoup as bs

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
    soup = bs(html, 'html')
    divs = soup.find('nav', class_='paginator')
    pages = divs.find_all('a', class_='paginator__btn')[-2].get('href')
    total_pages = pages.split('page=')[1].split('&')[0]
    return int(total_pages)


def get_data(html: str):
    """Ищет нужные данные на странице"""


def collect_data(total_pages: int, url):

    s = requests.Session()
    response = s.get(url=url, headers=headers)

    for i in range(1, total_pages + 1):
        pages = f'&page={i}'
        url = url + pages
        response = s.get(url=url, headers=headers)
        data = response.text
        print()


def main():

    price_from = 150000
    price_to = 250000
    url = f"https://krisha.kz/arenda/kvartiry/almaty/?das[_sys.hasphoto]=1&das[live.rooms][]=1&das[live.rooms][]=2&das[price][from]={price_from}&das[price][to]={price_to}&das[rent.period]=2&das[who]=1"
    html = get_html(url=url)
    write_html_in_file(html)
    total_pages = get_pages(html)
    collect_data(total_pages, url)
    print(total_pages)

if __name__ == '__main__':
    main()
