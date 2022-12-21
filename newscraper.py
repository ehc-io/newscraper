#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup, SoupStrainer
import requests
import argparse
import datetime
import time
import re
import os
import sys
import warnings
import string
import random

# Global
warnings.filterwarnings('ignore')
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0"
URL = "https://istoe.com.br/ultimas/"
MAX_ARTICLES = 10

def getrandomstring(N):
    return(''.join(random.choices(string.ascii_letters + string.digits, k=N)))

def main(runs, interval, nocache, showheaders, proxy, useragent,randomstring):
    COUNTER = 0
    headers = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language" : "en-US,en;q=0.5",
        "Connection" : "keep-alive",
        "DNT" : "1",
        "Sec-Fetch-Dest" : "document",
        "Sec-Fetch-Mode" : "navigate",
        "Sec-Fetch-Site" : "none",
        "Sec-Fetch-User" : "cross-site",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent" : useragent,
    }
    if proxy == None:
        proxies = None
    else:
        proxies = {"http": proxy, "https": proxy,}
    # 
    s = requests.Session()
    for i in range(1, int(runs)+1):
        print("======================< start of run #%s >======================" % i)
        if nocache:
            print('Sending "Cache-Control: no-cache, no-store" directive')
            headers['Cache-Control'] = "no-cache, no-store"
        now = datetime.datetime.now()
        article_counter = 0
        timestamp = int(time.time())
        if randomstring:
            url_param = "?q=" + getrandomstring(10)
        else:
            url_param = ""
        print("URL: %s" % URL + url_param)
        print("Timestamp: %s - %s" % (timestamp, now.time()))
        r = s.get(URL + url_param, headers=headers, proxies=proxies, verify=False)
        soupfilter = SoupStrainer("section")
        bs = BeautifulSoup(r.text, "html.parser", parse_only=soupfilter)
        article_tags = bs.find_all('article', {"class" :  "blocos-base" } )
        rexpr = re.compile("\d\d\/\d\d\/\d\d\s-\s\d+:\d+min")
        articles = list(zip(list((map(lambda x: re.match(rexpr, x.text[0:22].lstrip()).group(), article_tags))), list(map(lambda x: x.a.find("h1").text, article_tags))))
        # print response headers
        if showheaders:
            print("--------------------< Response Headers >------------------------ ")
            for key, value in r.headers.items():
                if key == "Cookies" or key == "link" or key == "Link" : continue
                print(key, ' : ', value)
        # print articles
        print("--------------------< Ultimas Noticias >------------------------ ")
        for article in articles :
            print('%s | %s' % (article[0] , article[1]))
            if article_counter > MAX_ARTICLES:
                break
            article_counter += 1
        print("=======================================================================")
        if int(runs) > 1 : time.sleep(int(interval))
        if i > int(runs) : break
        # r.close()
        # print('counter %s' % COUNTER)
        COUNTER += 1
        if COUNTER >= 2 : 
            os.system('clear')
            COUNTER = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="istoscrapper.py", description="Scrapper Istoe ultimas noticias ")
    parser.add_argument("-r", "--runs", nargs="?", const="dynamic", default=1, help=("Number of runs - loop"))
    parser.add_argument("-i", "--interval", nargs="?", const="dynamic", default="5", help=("Interval between runs"))
    parser.add_argument("-x", "--proxy", nargs="?", const="dynamic", default=None, help=("Proxy server - IP:PORT"))
    parser.add_argument("-nc", '--nocache', action='store_true', default=False, help=("Send Cache-Control no-cache directive"))
    parser.add_argument("-sh", '--showheaders', action='store_true', default=True, help=("Show response headers"))
    parser.add_argument("-p", '--randomstring', action='store_true', default=False, help=("Generates random string and passes it as an url parameter"))
    parser.add_argument("-u", "--useragent", nargs="?", const="dynamic", default=USER_AGENT, help=("User Agent"))
    args = parser.parse_args()    
    main(args.runs, args.interval, args.nocache, args.showheaders, args.proxy, args.useragent, args.randomstring)
