import requests
from bs4 import BeautifulSoup

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


def get_html(url: str):
    """ Получение кода страницы и преобразование его в html"""
    s = requests.Session()
    response = s.get(url=url, headers=headers)
    return response.text

def get_data(html: str):
    """
    Ищет данные на одной странице
    """
    soup = BeautifulSoup(html, 'html')
    divs = soup.find('section', class_='a-list a-search-list a-list-with-favs')
    ads = divs.find_all('div', class_='a-card__inc')
    result_data = []
    # for ad in ads:
    #     try:
    #         a = ad.find('a', class_='a-action a-action-favorite is-not-favorited')
    #         id = int(a.get('data-a-id'))
    #         print(id)
    #     except:
    #         id = ''
    #
    #
    #     data = {
    #             'id': id
    #
    #             }
    #     result_data.append(data)
    print(ads)


def main():

    price_from = 200000
    price_to = 220000
    url = f"https://krisha.kz/arenda/kvartiry/almaty/?das[_sys.hasphoto]=1&das[live.rooms][]=1&das[live.rooms][]=2&das[price][from]={price_from}&das[price][to]={price_to}&das[rent.period]=2&das[who]=1"
    html = get_html(url=url)
    get_data(html)


if __name__ == '__main__':
    main()