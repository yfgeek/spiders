# coding=utf-8
# python version：3.5
import json
import os
from concurrent.futures import ThreadPoolExecutor, wait
from requests import get, head


class Downloader:
    def __init__(self, url, file):
        self.url = url
        self.name = file
        self.failed = []

    def down(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/51.0.2704.103 Safari/537.36 "
        headers = {"User-Agent": user_agent, 'Referer': self.url}
        try:
            r = get(self.url, headers=headers, verify=False)
            print(self.name)
            with open('%s/whitepaper/%s.pdf' % (os.path.abspath(os.curdir), self.name), "wb") as fp:
                fp.write(r.content)
        except:
            self.failed.append(self.name)
            print(self.name + '失败了')
            pass


def read_from_pdf_list():
    f = open(
        '%s/whitepaper/white-paper-pdf.txt' % os.path.abspath(os.curdir), encoding='utf-8')
    list = json.load(f)
    body = ''
    for coin in list:
        name = coin['coin']
        if coin['name_cn'] != '－' and coin['name_cn'] != '-':
            name = name + '-' + coin['name_cn']
        print(coin['url'])
        # download = Downloader(coin['url'], name)

        # download.down()
    # print(self.failed)


if __name__ == "__main__":
    read_from_pdf_list()
