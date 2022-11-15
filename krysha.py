import json
import bs4
import requests
from datetime import date
import my_bd_command

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
    soup = bs4.BeautifulSoup(html, 'html.parser')
    divs = soup.find('nav', class_='paginator')
    pages = divs.find_all('a', class_='paginator__btn')[-2].get('href')
    total_pages = pages.split('page=')[1].split('&')[0]
    return int(total_pages)


def get_data(html: str, date):
    """
    Ищет данные на одной странице
    """
    soup = bs4.BeautifulSoup(html, 'html.parser')
    divs = soup.find('section', class_='a-list a-search-list a-list-with-favs')
    ads = divs.find_all('div', class_='a-card__inc')
    result_data = []
    for ad in ads:
        try:
            a = ad.find('a', class_='a-action a-action-favorite is-not-favorited')
            id_card = int(a.get('data-a-id'))
        except:
            id_card = ''
        try:
            div = ad.find('a', class_='a-card__title').text
            title = div.split(",")[0]
        except:
            title = ''
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
            zone = ad.find('div', class_='a-card__subtitle').text.strip().split(',')[0]
        except:
            zone = ''
        try:
            address = ad.find('div', class_='a-card__subtitle').text.strip().split(',')[1]
        except:
            address = ''
        try:
            description = ad.find('div', class_='a-card__text-preview').text.strip()
        except:
            description = ''
        try:
            div = ad.find('div', class_='card-stats').text.strip()
            publish_date = ' '.join(div.split()[1:])
        except:
            publish_date = ''
        try:
            div = ad.find('div', class_='a-card__header-left')
            url = "https://krisha.kz" + div.find('a').get('href')
        except:
            url = ''
            # вставляем запись в бд
        try:
            if my_bd_command.check_arenda(id_card) == 0:
                my_bd_command.insert_arenda(id_card, title, price, etaj, square, zone, address, description, url,
                                            publish_date)
                result_data.append({
                    'id_card': id_card,
                    'title': title,
                    'price': price,
                    'etaj': etaj,
                    'square': square,
                    'zone': zone,
                    'address': address,
                    'description': description,
                    'url': url,
                    'publish_date': publish_date
                })
                print('[INFO] Объявление добавлено в БД')
        except Exception as ex:
            print('[X] Ошибка вставки данных в бд: ', ex)
            continue
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
    my_bd_command.create_table()
    price_from = 0
    price_to = 90000000
    current_date = str(date.today())[-2:]
    room = '1'
    cities = 'almaty'
    url = f"https://krisha.kz/arenda/kvartiry/{cities}/?das[_sys.hasphoto]=1&das[live.rooms][]={room}&das[price][from]={price_from}&das[price][to]={price_to}&das[rent.period]=2&das[who]=1"
    html = get_html(url=url)
    # write_html_in_file(html)
    total_pages = get_pages(html)
    collect_data(total_pages, url, current_date)
    get_data(html, current_date)


if __name__ == '__main__':
    main()
