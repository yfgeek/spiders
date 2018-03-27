# coding=utf-8
# python version：2.7
import json
import os
import urllib2
import re
from bs4 import BeautifulSoup as BS


class Spider(object):
    def __init__(self):
        self.list = list()
        self.id = 0

    def get_coin_list(self, page):
        url = 'https://www.feixiaohao.com/list_%s.html' % page

        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
        except urllib2.HttpError, e:
            print e.code
            exit(0)
        except urllib2.URLError, e:
            print e.reason
            exit(0)

        html = response.read()
        soup = BS(html, "lxml")
        table = soup.find("table", {
            "class": "table maintable"
        })
        td_th = re.compile('t[dh]')

        for row in table.findAll("tr"):
            if row.get('id'):
              self.list.append(row.get('id'))

    def download_all_list(self):
        for coin in self.list:
            print coin
            content = self.download(coin)
            self.write_file(coin, content)

    def run(self, page):
        for x in range(1, page):
            self.get_coin_list(x)
        self.download_all_list()

    def download(self, coin_name):
        url = 'https://www.feixiaohao.com/currencies/%s' % coin_name
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
        except urllib2.HttpError, e:
            return
        except urllib2.URLError, e:
            return
        html = response.read()
        soup = BS(html, "lxml")
        des = soup.find("div", {
            "class": 'des'
        }).get_text().strip().replace(u'查看全部', '')
        print des

        ul = soup.find_all("div", {
            "class": "secondPark"
        })[0].find_all("span", {
            "class": "value"
        })
        name_en = ul[0].text
        name_cn = ul[1].text
        time = ul[3].text
        whitepaper = ul[4].find_all("a")[0].attrs['href'] if ul[4].find_all("a") else '-'
        website = []
        website_list = ul[5].find_all("a") if ul[5].find_all("a") else []
        blockchain = []
        blockchain_list = ul[6].find_all("a") if ul[6].find_all("a") else []
        for web in website_list:
            website.append(web.attrs['href'])
        for block in blockchain_list:
            blockchain.append(block.attrs['href'])
        content = {
            'id' : self.id,
            'name': coin_name,
            'name_en': name_en,
            'name_cn': name_cn,
            'time': time,
            'whitepaper': whitepaper,
            'website': website,
            'blockchain': blockchain,
        }
        return content

    def write_file(self, coin_name, content):
        if not coin_name:
            return
        f = open(
            '%s/coins/%d-%s.txt' % (os.path.abspath(os.curdir), self.id, coin_name), 'w')
        js = json.dumps(content, sort_keys=True, indent=4, separators=(',', ':'))
        f.write(js)
        self.id = self.id + 1
        f.close()


if __name__ == "__main__":
    obj_spider = Spider()
    obj_spider.run(21)
