#coding=utf-8
#python version：2.7
import pymysql

class UrlManager(object):
    def __init__(self):
        self.new_urls = dict()  # 待爬取url
        self.old_urls = dict()  # 已爬取url
        self.db = pymysql.connect("localhost", "root", "", "uob" ,use_unicode=True, charset="utf8")
        self.cursor = self.db.cursor()

    def add_new_url(self, name, url, description):  # 向管理器中添加一个新的url
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls[name] = url
            sql = u"INSERT INTO list_ky (name,  url, description) VALUES (\"" + name  +  u"\", \"" + url + u"\", \"" + description + u"\");"

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
