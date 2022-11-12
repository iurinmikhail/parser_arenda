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
            start = ad.find('div', class_='card-stats').text.strip()
            start_data = ' '.join(start.split()[1:])
        except:
            start_data = ''
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
                'start': start_data
                }
        result_data.append(data)



def main():

    price_from = 200000
    price_to = 200000
    url = f"https://krisha.kz/arenda/kvartiry/almaty/?das[_sys.hasphoto]=1&das[live.rooms][]=1&das[live.rooms][]=2&das[price][from]={price_from}&das[price][to]={price_to}&das[rent.period]=2&das[who]=1"
    html = get_html(url=url)
    get_data(html)


if __name__ == '__main__':
    main()