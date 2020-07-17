import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 YaBrowser/20.4.3.268 (beta) Yowser/2.5 Safari/537.36', 'accept': '*/*'}

def get_html(url):
    r = requests.get(url, headers = HEADERS)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('div', class_='cmc-table').find_all('tr', class_ = 'cmc-table-row')

    links = []

    for tr in trs:
        a = tr.find('a').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)

    return links

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1').text.strip()
    except:
        name = ''

    try:
        price = soup.find('span', class_= 'cmc-details-panel-price__price').text.strip()
    except:
        price = ''

    data = {'name': name,
            'price': price}
    return data

def write_csv(data):
    with open('coinmarket.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['name'],
                         data['price']))
        print(data['name'], 'parsed')

def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all/'

    all_links = get_all_links(get_html(url))

    for url in all_links:

        html = get_html(url)
        data = get_page_data(html)
        write_csv(data)

    end =datetime.now()

    total = end - start
    print(str(total))







if __name__ == '__main__':
    main()