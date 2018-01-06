# -*- coding: utf-8 -*-
# Code by Ivan
import time
import pymysql
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def clean(text):
    return text.strip('\n').strip(' ').strip('  ').strip('\t').strip('\r')

if __name__ == '__main__':
    default_encoding = 'utf-8'
    if sys.getdefaultencoding() != default_encoding:
        reload(sys)
        sys.setdefaultencoding(default_encoding)

        db = pymysql.connect("localhost", "root", "", "price", use_unicode=True, charset="utf8")
        cursor = db.cursor()
        database_name = "relation"

        browser = webdriver.Safari()
        browser.get('http://www.yiqiyin.com/login')

        login = browser.find_element_by_name("mobile")
        password = browser.find_element_by_name("password")

        login.send_keys("")
        password.send_keys(123456)
        password.send_keys(Keys.RETURN)

        time.sleep(2)

        # different product
        browser.get('http://www.yiqiyin.com/product_catalogs/1/products/39/orders/new')
        time.sleep(2)

        selection = browser.find_element_by_class_name("product-selection").find_elements_by_class_name("col-md-2")
        for div_sec in selection:
            sector = div_sec.find_element_by_class_name("product-name").find_elements_by_tag_name("li")
            mod = list()
            for product in sector:
                product_item = clean(product.find_elements_by_tag_name("a")[0].text)
                if product.find_elements_by_tag_name("a")[0].get_attribute('id'):
                    print product_item, product.find_elements_by_tag_name("a")[0].get_attribute('id')
                    product_id = product.find_elements_by_tag_name("a")[0].get_attribute('id').strip("sku_")
                    mod.append(product_id)
                    if float(product_id):
                        sql = u"INSERT INTO " + database_name + u" (id,value) VALUES (\"" \
                          + str(product_id) + u"\", \""  + str(product_item) + u"\");"
                        try:
                            cursor.execute(sql)
                            db.commit()
                        except:
                            pass




            print "["+",".join(mod)+"]" + "\n"
