from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from pprint import pprint

number_id = {}
reponse = urlopen('https://krisha.kz/arenda/kvartiry/almaty/?areas=&das[_sys.hasphoto]=1&das[live.rooms]=1&das[price][from]=150000&das[price][to]=250000&das[rent.period]=2&das[who]=1&lat=43.23621&lon=76.92370&zoom=14')
html = reponse.read().decode('utf-8')
soup = bs(html)
for link in soup.find_all('nav'):
    print(link)
    # s= link.get('paginator')
    # if s.startswith('/a/show/'):
    #     number_id.setdefault(int(s.split('/')[3]))

pprint(number_id)
