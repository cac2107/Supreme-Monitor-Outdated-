import json
import requests
import bs4
import time
import httpmonitor
import datetime
import pytz

Temp = {}
Hooks = []

WEBHOOK = "ENTER YOUR WEBHOOK"

def webhookSender():
    while True:
        if len(Hooks) != 0:
            for message in Hooks:
                img, desc = message
                webhook(img, desc)
                time.sleep(1)
        time.sleep(3)


def infoGrabber(soup):
    data = json.loads(soup.text)
    info = {}

    for style in data["styles"]:
        idd = {}
        sizes = {}
        idd["image"] = style["image_url"]
        for size in style["sizes"]:
            if size["stock_level"] == 1:
                sizes[str(size["name"])] = size["id"]
        
        idd["color"] = style["name"]
        idd["sizes"] = sizes
        info[str(style["id"])] = idd
    return info


def createURL(style, size):
    # Uses old html code for auto carts that no longer works
    # Domain no longer active
    url = f"http://resalometer.com/?style={style}&size={size}&product=185489"
    return url


def webhook(url, desc):
    message = {
        'username': 'Supreme Monitor',
        'content': '',
        'avatar_url': 'https://i.ibb.co/5K7WpcH/image0.png'
    }
    message["embeds"] = []
    embed = {}
    embed["description"] = desc
    currentUTCTime = pytz.utc.localize(datetime.datetime.utcnow())
    currentTime = currentUTCTime.astimezone(pytz.timezone('US/Eastern'))
    footer = {"text": "Resalometer | " + str(currentTime)}
    embed["footer"] = footer
    image = {"url": "http:" + url}
    embed["image"] = image
    fields = [{"name": "\u200B", "value": " | [StockX]" + "(https://anidiots.guide/first-bot/using-embeds-in-messages)"}]
    embed["fields"] = fields
    message["embeds"].append(embed)

    wbhook = WEBHOOK
    result = requests.post(wbhook, data=json.dumps(message), headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        time.sleep(3)
        webhook(url, desc)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


def existsInTemp(styleid, sizes):
    if styleid not in Temp:
        Temp[styleid] = sizes
        return False
    elif Temp[styleid] == sizes:
        return True
    else:
        for size in sizes:
            if size not in Temp[styleid]:
                Temp[styleid] = sizes
                return False
            else:
                Temp[styleid] = sizes
                return True


def getName(jsonid, color):
    with open('products.txt', 'r') as p:
        jsonfile = p.read()
    products = json.loads(jsonfile)

    for prod in products:
        if prod == jsonid:
            return products[prod]


def newGetName(jsonid):
    products = httpmonitor.returnProducts()
    for prod in products:
        if prod == jsonid:
            return products[prod]


def jsonMessage(styleid, color, img, sizes, url):
    newurl = str(url.rsplit('/', 1)[1])
    jsonid = str(newurl.rsplit('.', 1)[0])
    name = newGetName(jsonid)
    desc = f"**{name}**\n**{color}**\n**Sizes:**\n"
    for size in sizes:
        url = createURL(styleid, sizes[size])
        if size == "N/A":
            sizet = "\n"
        else:
            sizet = f"[{str(size)}]({str(url)})\n"
        desc = desc + sizet
    hookertup = (img, desc)
    Hooks.append(hookertup)


def jsonMonitor(url):
    while True:
        url = "https://www.supremenewyork.com" + url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        r = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        info = infoGrabber(soup)
        print("JSON WOrking")

        for sizecode in info:
            sizeid = str(sizecode)
            color = info[sizecode]["color"]
            img = info[sizecode]["image"]
            sizes = info[sizecode]["sizes"]

            if existsInTemp(sizeid, sizes) is False:
                if len(sizes) != 0:
                    jsonMessage(sizeid, color, img, sizes, url)

            time.sleep(15)
