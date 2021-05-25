# -*- coding: utf-8 -*-
# @Time    : 2020/7/13 15:08
# @Software: PyCharm


import json
import time
import random
import base64
import datetime
import requests
from Crypto.Cipher import DES3
import pymysql
from faker import Factory
import math
from concurrent.futures import ThreadPoolExecutor,as_completed,ProcessPoolExecutor
import calendar
import traceback
BS = DES3.block_size
def pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

def unpad(s):
    return s[0:-ord(s[-1])]

class Des(object):

    @staticmethod
    def encrypt(text, key):
        """
        加密处理
        :param text:
        :param key:
        :return:
        """
        text = pad(text)
        iv = datetime.datetime.now().strftime('%Y%m%d').encode()
        cryptor = DES3.new(key, DES3.MODE_CBC, iv)
        # self.iv 为 IV 即偏移量
        x = len(text) % 8
        if x != 0:
            text = text + '\0' * (8 - x)  # 不满16，32，64位补0
        # print(text)
        ciphertext = cryptor.encrypt(text.encode('utf-8'))
        return base64.standard_b64encode(ciphertext).decode("utf-8")

    @staticmethod
    def decrypt(text,key):
        """
        解密处理
        :param text:
        :param key:
        :return:
        """
        iv = datetime.datetime.now().strftime('%Y%m%d').encode()
        cryptor = DES3.new(key, DES3.MODE_CBC, iv)
        de_text = base64.standard_b64decode(text)
        plain_text = cryptor.decrypt(de_text)
        st = str(plain_text.decode("utf-8"))
        out = unpad(st)
        return out




class wenshu():

    des = Des()

    def time_now(self):
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def time_now_2(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def make_ciphertext(self):
        """
        加密字段ciphertext
        :return:
        """
        timestamp = str(int(time.time() * 1000))
        salt = ''.join([random.choice('0123456789qwertyuiopasdfghjklzxcvbnm') for _ in range(24)])
        iv = datetime.datetime.now().strftime('%Y%m%d')
        enc = self.des.encrypt(timestamp, salt)
        strs = salt + iv + enc
        result = []
        for i in strs:
            result.append(bin(ord(i))[2:])
            result.append(' ')
        return ''.join(result[:-1])


    def request_c(self,method,url,headers,payload,user_proxies=True):
        for i in range(5):
            try:
                response = requests.request(method, url, headers=headers, data = payload,timeout=10)
                response.encoding='utf-8'
                return json.loads(response.text)
            except Exception as e:
                print(e)
                time.sleep(5)



    def get_docid(self,queryCondition,page=1,pages=None):
        print('当前爬取是的是第{}页，总共{}页'.format(page,pages))
        """
        获取文书的docid
        :return:
        """
        try:
            time_now=self.time_now()
            query={
                "id": time_now,
                "command": "queryDoc",
                "params": {
                    "pageNum": page,
                    "sortFields": "s50:desc",
                    "ciphertext": self.make_ciphertext(),
                    "devid": "",
                    "devtype": "1",
                    "pageSize": "200",
                    "queryCondition": queryCondition
                }
            }
            try:
                # 把请求的body进行加密处理
                token=self.request_c("POST",url='http://47.102.159.7:8080/wenshu',headers={'Content-Type': 'text/plain'},payload=str(query),user_proxies=False)['data']['token']
                # 请求文书的app接口
                url = "http://wenshuapp.court.gov.cn/appinterface/rest.q4w"
                payload = {'request': token}
                headers = {
                  'User-Agent': Factory.create().user_agent(),
                  'Host':  'wenshuapp.court.gov.cn',
                }
                content=self.request_c("POST", url, headers,payload)
            except Exception as e:
                print(traceback.format_exc())
                print('请求出错了',e)
                self.get_docid(queryCondition,page,pages)
            if str(content['ret']['code'])=='1':
                # 返回的参数是加密的字段，需进行解密处理
                text=content['data']['content']  #加密的文本信息
                key=content['data']['secretKey']  #加密的key
                res=json.loads(self.des.decrypt(text,key))
                resultCount=res['queryResult']['resultCount']   #按当前条件筛选的文书有多少数量
                docinfo_list =res['queryResult']['resultList']  #文书的docid列表
                if len(docinfo_list)==0 and page==1:
                    self.get_docid(queryCondition,page,pages)
                if len(docinfo_list)==0 and page<50:
                    self.get_docid(queryCondition, page, pages)
                for doc in docinfo_list:
                    docid=doc['rowkey']
                    print(self.time_now_2(), docid)
                if pages==None:
                    pages=math.ceil(resultCount/200)   #获取总的页数
                if page<pages and page<50:  #循环调用
                    page+=1
                    self.get_docid(queryCondition,page,pages)
            else:
                print('已出现错误',content['ret'])
                self.get_docid(queryCondition,page, pages)
        except Exception as e:
            print(e)
            self.get_docid(queryCondition, page, pages)


    def get_article(self,docid):
        try:
            time_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            query ={
                "id": time_now,
                "command": "docInfoSearch",
                "params": {
                    "ciphertext": self.make_ciphertext(),
                    "docId": docid,
                    "devtype": "1",
                    "devid": ""
                }
            }
            # 把请求的body进行加密处理，
            try:
                token = self.request_c("POST", url='http://47.102.159.7:8080/wenshu', headers={'Content-Type': 'text/plain'},payload=str(query))['data']['token']
                # 请求文书的app接口
                url = "http://wenshuapp.court.gov.cn/appinterface/rest.q4w"
                payload = {
                  'request': token}
                headers = {
                  'User-Agent': Factory.create().user_agent(),
                  'Host': 'wenshuapp.court.gov.cn',
                }
                content = self.request_c("POST", url, headers, payload)
            except Exception as e:
                print('请求出错了',e)
                self.get_article(docid)
            if str(content['ret']['code'])=='1':
                text = content['data']['content']  # 加密的文本信息
                key = content['data']['secretKey']  # 加密的key
                result = self.des.decrypt(text, key)
                content = pymysql.escape_string(result)
                print(self.time_now_2(),content)
            else:
                print('已出现错误',content['ret'])
                self.get_article(docid)
        except Exception as e:
            print(e)
            self.get_article(docid)


if __name__ == '__main__':
    server=wenshu()
    # _________________爬取文书的docid____________________
    queryCondition = [{"key": "cprqEnd", "value": "2020-09-11"}, {"key": "cprqStart", "value": "2020-09-11"}]
    server.get_docid(queryCondition=list(queryCondition))


    # _________________爬取文书的详情____________________
    server.get_article('73e7a1998246480eac7eabef012a22ef')


