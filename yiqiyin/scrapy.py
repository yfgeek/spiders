# -*- coding: utf-8 -*-
# Code by Ivan

import os
import re
import sys
import urllib
import urllib2
import time
import cookielib
from bs4 import BeautifulSoup
import pymysql

import json

class Go(object):
    # Initializaiton Constructor
    def __init__(self,database_name):
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(self.opener)
        getCookieUrl = "http://www.yiqiyin.com/login"
        self.html = urllib2.urlopen(getCookieUrl).read()

        self.db = pymysql.connect("localhost", "root", "", "price" , use_unicode=True, charset="utf8")
        self.cursor = self.db.cursor()
        self.database_name = database_name

    # Browse the page to get Cookie
    def _get_headers(self, referer):
        headers = {}
        headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        headers['Connection'] = 'keep-alive'
        headers['Cache-Control'] = 'max-age=0'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6'
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        headers['Referer'] = referer
        return headers

    # sign in github.com
    def login(self):
        soup = BeautifulSoup(self.html, "lxml")
        token = soup.find(attrs={"name": "csrf-token"})['content']
        print token

        loginparams = {
            'utf8': '✓',
            'mobile': '',
            'password': '123456',
            'authenticity_token': token
        }
        # post loginparams to login
        req = urllib2.Request('http://www.yiqiyin.com/session/create', urllib.urlencode(loginparams),
                              headers=self._get_headers('http://www.yiqiyin.com/session/create'))
        try:
            resp = urllib2.urlopen(req)
        except:
            print "跳过一条"
            pass
        self.operate = self.opener.open(req)
        thePage = resp.read().decode("utf-8")
        # print the result of login
        print "Login Successful \n"
        self.html = thePage
        return thePage

    def getinfo(self, product, size, material, side, amount, tech):
        print product, size, material, side, amount, tech
        time.sleep(0.5)
        soup = BeautifulSoup(self.html, "lxml")
        token = soup.find(attrs={"name": "csrf-token"})['content']
        print token
        params = {
            'utf8': '✓',
            'authenticity_token': token,
            'order[options][is_use_baitiao]': 0,
            'order[options][size]': size,
            'order[options][material]': material,
            'order[options][s_d_side]': side,
            'order[options][tech][]': tech,
            'order[options][amount]': amount,
            'order[options][amount_input]': '',
            'order[options][size_input]': '',
            'order[options][product_id]': product,
        }

        req = urllib2.Request('http://www.yiqiyin.com/orders/price', urllib.urlencode(params),
                              headers=self._get_headers('http://www.yiqiyin.com/orders/price'))
        tmp = 0
        try:
            resp = urllib2.urlopen(req)
            result = resp.read().decode("utf-8")
            data = json.loads(result)["data"]
            sql = u"INSERT INTO " + self.database_name  +" (price,  base, addition, discount_name, is_use_discount, discounted_price, product, size, material, side, amount, tech) VALUES (\"" \
                  + str(data["price"]) + u"\", \"" + str(data["base"]) + u"\", \"" + str(
                data["addition"]) + u"\", \"" + str(data["discount_name"]) + u"\", \"" + str(data["is_use_discount"]) \
                  + u"\", \"" + str(data["discounted_price"]) + u"\", \"" + str(product) + u"\", \"" + str(
                size) + u"\", \"" + str(material) + u"\", \"" + str(side) + u"\", \"" + str(amount) + u"\", \"" + str(
                tech) + u"\");"

            print sql
            try:
                # 执行sql语句
                self.cursor.execute(sql)
                # 提交到数据库执行
                self.db.commit()
                # print "success"
            except:
                # Rollback in case there is any error
                self.db.rollback()
                print "error"

            # print the result of login
            print result
        except:
            print "跳过一条"
            pass


if __name__ == '__main__':
    default_encoding = 'utf-8'
    if sys.getdefaultencoding() != default_encoding:
        reload(sys)
        sys.setdefaultencoding(default_encoding)

        # database name
        ga = Go("product_39")
        # login
        ga.login()

        # different product should have different arrays
        size = [1, 802, 803, 280]
        product = 39
        material = [1887, 18, 1888, 1199]
        side = [71, 70]
        amount = [56, 57, 58, 146, 2697]
        tech = [46, 168, 2644, 170, 169, 524, 352]

        for s in size:
            for m in material:
                for sd in side:
                    for a in amount:
                        for t in tech:
                            ga.getinfo(product, s, m, sd, a, t)
