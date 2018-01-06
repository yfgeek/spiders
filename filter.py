# coding=utf-8
# python version：2.7

from sqlalchemy import create_engine

from jpype import *
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')

import pymysql
from pybloomfilter import BloomFilter


class Filter(object):
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "", "uob", use_unicode=True, charset="utf8")
        self.engine = create_engine('mysql+pymysql://root:@localhost:3306/uob?charset=utf8')

        self.cursor = self.db.cursor()
        self.bfilter = BloomFilter(1000, 0.001, 'uob.bloom')
        startJVM(getDefaultJVMPath(),
                 "-Djava.class.path=/Users/ivan/d/uobspider/hanlp-1.3.5.jar:/Users/ivan/d/uobspider/",
                 "-Xms1g", "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:

    def distinct(self):
        sql = "SELECT * FROM list;"
        allData = pd.read_sql(sql, con=self.engine)  # 从抓取过来的数据库读入
        allData.drop_duplicates('name', 'first', inplace=True)  # 去除重复name
        allData.drop_duplicates('url', 'first', inplace=True)  # 去除重复url
        allData.reset_index(drop=True, inplace=True)  # index重新计数
        print allData.detail()
        allData.to_sql('first_filter', self.engine, if_exists='replace', index=True, index_label='fid')  # 输出到新的数据库表
        return allData

    def insertData(self, id, name, url):
        insertsql = "INSERT INTO filter_second (list_id,name,url) VALUES(" + str(id) + ",\"" + str(
            name) + "\",\"" + str(url) + "\");"
        print insertsql
        try:
            self.cursor.execute(insertsql)
            self.db.commit()
        except:
            self.db.rollback()
            print "error"

    def filterHMM(self):
        sql = "SELECT id,name,url FROM list;"
        self.cursor.execute(sql)
        allData = self.cursor.fetchall()
        JDClass = JClass("com.hankcs.hanlp.seg.CRF.CRFSegment")
        jd = JDClass().enableNameRecognize(True)
        names = []
        for data in allData:
            s = data[1]
            words = jd.seg(jpype.JString(s))
            for i in words:
                if "nr" in str(i.nature):
                    tmp = str(i.word)
                    if len(tmp) > 1:
                        self.insertData(data[0], data[1], data[2])
                        break


if __name__ == "__main__":
    obj_filter = Filter()
    obj_filter.distinct()
    obj_filter.filterHMM()
