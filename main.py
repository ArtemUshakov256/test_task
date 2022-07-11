import requests
from bs4 import BeautifulSoup
import csv
import logging


logging.basicConfig(level=logging.INFO)


query = input("Введите поисковой запрос\n")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5 Safari/537.36",
}


def get_card_url(query):
    params = {"search": query}
    response = requests.get(url="https://novex.ru/search/", headers=headers, params=params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("div", class_="col-4 col-md-4 col-sm-6 col-xs-12")
        for card in data:
            url = "https://novex.ru" + card.find("a").get("href")
            yield url
    else:
        return None


data = []


try:
    for card_url in get_card_url(query):
        response = requests.get(url=card_url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        name = soup.find("h1").text
        trade_mark = soup.find("div", class_="vocabulary-list__value").text
        city = "Санкт-Петербург"
        price_list = soup.find_all("span", class_="price")
        price_form = price_list[-1].text
        price = price_form[:-2] + ", " + price_form[-2:]
        data.append([name, trade_mark, city, price])
except Exception as e:
    logging.error(e)


with open("goods_data.csv", "w", encoding="cp1251") as file:
    writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    for info in data:
        writer.writerow(info)
