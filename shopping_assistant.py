import json
from urllib import request
from lxml import html
import re
from threading import Thread


def prepare_tree(url):
    html_doc = request.urlopen(url).read()
    tree = html.fromstring(html_doc)
    return tree


def get_price(xpath, tree):
    price = tree.xpath(xpath)[0].text_content()
    try:
        price = float(price)
    except:
        price = re.findall('\d+,\d{2}', price)[0]
        price = price.replace(',', '.')
        price = float(price)
    return price


def get_price_sum(shop, data, xpaths):
    shopping_sum = []
    for index, url in enumerate(data[shop]["urls"]):
        tree = prepare_tree(url[0])
        price = get_price(xpaths[shop], tree) * url[1]
        shopping_sum.append(price)
    suma = sum(shopping_sum)
    sum_with_shipping = suma + data[shop]["shipping"]
    print("Shop: ", shop)
    print("Suma bez dopravy: ", suma)
    print("Doprava: ", data[shop]["shipping"])
    print("Cena s dopravou: ", sum_with_shipping)
    print("======================================")
    return shopping_sum

with open('data.json') as data_file:
    data = json.load(data_file)

with open('xpath.json') as xpaths_file:
    xpaths = json.load(xpaths_file)

for key in data:
    if key != "tesco":
        continue
    thread = Thread(target=get_price_sum, args=(key, data, xpaths))
    thread.start()


