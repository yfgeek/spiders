#coding=utf-8
#python version：2.7

import urllib
import urllib2
import time
from bs4 import BeautifulSoup as BS

from urlmanager import UrlManager

class Spider(object):
    def __init__(self):
        self.urls = UrlManager()    #url管理器

    def baidusearch(self,word,page):
        baseUrl = 'http://www.baidu.com/s'

        data = {'wd': word, 'pn': str(page - 1) + '0', 'tn': 'baidurt', 'ie': 'utf-8', 'bsst': '1'}
        data = urllib.urlencode(data)
        url = baseUrl + '?' + data

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
        td = soup.find_all(class_='f')

        for t in td:
            name = t.h3.a.get_text().replace(' ', '').replace('	', '').replace('\n', '').replace(u'_百度百科','')
            # print name
            url = t.h3.a['href'].replace(' ', '').replace('\n', '')

            # print url

            font_str = t.find_all('font', attrs={'size': '-1'})[0].get_text()
            start = 0  # 起始
            realtime = t.find_all('div', attrs={'class': 'realtime'})
            if realtime:
                realtime_str = realtime[0].get_text()
                start = len(realtime_str)
                # print realtime_str
            end = font_str.find('...')
            # print font_str[start:end+3],'\n'
            self.urls.add_new_url(name, url, font_str[start:end+3].replace(' ', '').replace('	', '').replace('\n', ''))

    def craw(self, root_url):
        count = 1 #判断当前爬取的是第几个url
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():      #循环,爬取所有相关页面,判断异常情况
            try:
                new_url = self.urls.get_new_url()   #取得url
                print('craw %d : %s' % (count, new_url))  # 打印当前是第几个url
                html_cont = self.downloader.download(new_url)   #下载页面数据
                new_urls, new_data = self.parser.parse(new_url,html_cont)    #进行页面解析得到新的url以及数据

                self.urls.add_new_urls(new_urls) #添加新的url
                self.outputer.collect_data(new_data) #收集数据

                if count == 10:  # 此处10可以改为100甚至更多,代表循环次数
                    break

                count = count + 1
            except:
                print('craw failed')

        self.outputer.output_html()   #利用outputer输出收集好的数据

if __name__=="__main__":
    obj_spider = Spider()
    for x in range(1,200):
        obj_spider.baidusearch('中国矿业大学 site:baike.baidu.com', x)
        time.sleep(3)
