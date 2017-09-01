# -*- coding: utf-8 -*-

import requests
from scrapy.selector import Selector
import json
import time
"""
西刺代理
"""

def crawl_ip():


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
    }

    ip_list = []
    for i in range(4):
        time.sleep(1)
        response = requests.get("http://www.xicidaili.com/nn/{0}".format(i),headers=headers)
        selector = Selector(text=response.text)
        all_trs = selector.css("#ip_list tr")

        for tr in all_trs:
            speed_str = tr.css(".bar::attr(title)").extract_first()
            if speed_str:
                speed = float(speed_str.split("秒")[0])
                all_texts =tr.css("td::text").extract()

                ip = all_texts[0]
                port = all_texts[1]
                proxy_type = all_texts[5]

                ip_list.append((ip,port,proxy_type,speed))
    with open("ips.txt","w",encoding="utf-8") as f:
        f.write(json.dumps(ip_list))
        f.close()

# print(crawl_ip())


def get_random_proxy():
    with open('ips.txt',encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data

# get_random_proxy()