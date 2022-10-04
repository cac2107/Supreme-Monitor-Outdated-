import requests
import bs4
import time
import re
import json
import threading
from jsonmonitor import jsonMonitor

Products = {}

l = open('jsons.txt', 'r')
Jsons = l.readlines()
l.close()

def productsInitiator(url, name):
    with open('products.json', 'r') as p:
        jsonfile = p.read()

    if jsonfile == '':
        products = {}
    else:
        products = json.loads(jsonfile)
        products[url] = name
    newJson = json.dumps(products)
    
    with open('products.json', 'w') as p:
        p.write(newJson)


def newProductsInitiator(url, name):
    Products[url] = name


def existsInJson(link):
    exists = False
    for Json in Jsons:
        if Json == link:
            exists = True
    return exists


def jsonModifier(link):
    with open('jsons.txt', 'a', newline='\n') as p:
        p.write(link + "\n")


def newJsonThread(url):
    thread = threading.Thread(target=jsonMonitor, args=(url,))
    thread.start()


def returnProducts():
    return Products


def htmlMonitor(url):
    while True:
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, 'lxml')
        result = soup.find_all('div', class_="inner-article")
        for item in result:
            name = item.find('div', class_="product-name")
            link = name.find(href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
            jsonLink = str(link.rsplit('/', 1)[0]) + ".json"
            jsonID = str((str(link.rsplit('/', 2)[1])).rsplit('/', 1)[0])
            print("HTML Working")

            newProductsInitiator(jsonID, name.text)

            if existsInJson(jsonLink) is False:
                Jsons.append(jsonLink)
                jsonModifier(jsonLink)
                newJsonThread(jsonLink)
        time.sleep(300)
