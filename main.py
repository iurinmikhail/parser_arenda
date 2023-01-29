from datetime import date

from my_bd_command import *
from krysha import get_html, get_pages, collect_data, get_data

def main():
    price_from = 0
    price_to = 90000000
    db_path = "arenda_bd.db"
    room = ''
    cities = 'almaty'
    current_date = str(date.today())[-2:]
    url = f"https://krisha.kz/arenda/kvartiry/{cities}/?das[_sys.hasphoto]=1&das[live.rooms][]={room}&das[price][from]={price_from}&das[price][to]={price_to}&das[rent.period]=2&das[who]=1"

    sq = CommandSQlite(db_path)
    create_table_command = """
        CREATE TABLE IF NOT EXISTS arenda(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_card INT,
        title TEXT,
        price TEXT,
        etaj TEXT,
        square TEXT,
        zone TEXT,
        address TEXT,
        description TEXT,
        url TEXT,
        publish_date TEXT,
        parsing_date DATE
        );"""
    sq.execute_query(create_table_command)
    html = get_html(url=url)
    # write_html_in_file(html)
    total_pages = get_pages(html)
    collect_data(total_pages, url, current_date)
    get_data(html, current_date)

main()