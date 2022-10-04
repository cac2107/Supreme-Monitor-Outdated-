from httpmonitor import *
from jsonmonitor import *
import threading

threads = []

linksss = ["https://www.supremenewyork.com/shop/all/jackets", 
"https://www.supremenewyork.com/shop/all/shirts", 
"https://www.supremenewyork.com/shop/all/tops_sweaters", 
"https://www.supremenewyork.com/shop/all/sweatshirts", 
"https://www.supremenewyork.com/shop/all/shorts", 
"https://www.supremenewyork.com/shop/all/hats", 
"https://www.supremenewyork.com/shop/all/bags", 
"https://www.supremenewyork.com/shop/all/accessories", 
"https://www.supremenewyork.com/shop/all/shoes", 
"https://www.supremenewyork.com/shop/all/skate"]

for link2 in linksss:
    thread = threading.Thread(target=htmlMonitor, args=(link2,))
    threads.append(thread)

webhookThread = threading.Thread(target=webhookSender)
threads.append(webhookThread)

for thread in threads:
    thread.start()
