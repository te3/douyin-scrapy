# -*- coding:utf-8 -*-

import time
from douyin.Verification import encryption, getXGon, x_gorgon, str_to_byte
from douyin.pipelines import engine
import jieba
import redis
from douyin.utils.ifs import is_chinese


class RequestsStructure(object):
    """ 处理请求头中的header """
    def __init__(self, params,
                 cookies='install_id=1310263726846926; ttreq=1$bf4ffabd609e4faac791887df5c3509bdde1a78b; SLARDAR_WEB_ID=fd6c87fd-cfbc-4d36-8275-83d1bca164d2; passport_csrf_token=e1faac7f0b1213104059242ab6c0ab01; d_ticket=7d5878a2191c973858b9242bc6f190162a304; odin_tt=7f20ecc4e486ab28d2a59054a2d782801b06738b56aff5b3947a7684c5c85c5381c09474e96692c5ca3dab2228b909900b0408a326a81b7440c03f3332bd463e; sid_guard=751e2e12c6fb7a86ae0085986e65dc38%7C1591273883%7C5184000%7CMon%2C+03-Aug-2020+12%3A31%3A23+GMT; uid_tt=be26f55d2b0374ad46bedde2af47e74f; sid_tt=751e2e12c6fb7a86ae0085986e65dc38; sessionid=751e2e12c6fb7a86ae0085986e65dc38',
                 x_tt_token='00751e2e12c6fb7a86ae0085986e65dc381215edce6b8495055a06e9cee59faeab26699bf1ad949f1ad0737923cadbfde955'):

        self.cookies = cookies
        self.x_tt_token = x_tt_token
        self.header = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            'X-SS-STUB': self.stub(params),
            'X-SS-REQ-TICKET': self.time_stamp(1000),
            'sdk-version': "1",
            'X-Gorgon': self.x_gorgon(params),
            "Cookie": self.cookies,
            "X-tt-token": self.x_tt_token,
            'X-Khronos': self.time_stamp(),
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Host': "api.amemv.com",
            'User-Agent': "okhttp/3.10.0.1",
            'cache-control': "no-cache",
        }



    def get_header(self, *args, **kwargs):
        for i in kwargs:
            self.header[i] = kwargs[i]
        return self.header

    @staticmethod
    def time_stamp(unit=1):
        time_stamp = str(time.time() * unit).split(".")[0]
        return time_stamp

    @staticmethod
    def stub(params):
        return encryption(params)

    def x_gorgon(self, params):
        ts = self.time_stamp()
        s = getXGon(params, self.stub(params))
        gorgon = x_gorgon(ts, str_to_byte(s))
        return gorgon


class FormStructure(object):
    def __init__(self):
        self.form = {
            'sec_user_id': '',
            'address_book_access': "1",
            'retry_type': 'no_retry',
            'iid': '2576896581967031',
            'device_id': '3491689742481495',
            'ac': 'wifi',
            'channel': 'tengxun_new',
            'aid': '1128',
            'app_name': 'aweme',
            'version_code': '830',
            'version_name': '8.3.0',
            'device_platform': 'android',
            'ssmix': 'a',
            'device_type': 'MI+5s',
            'device_brand': 'Xiaomi',
            'language': 'zh',
            'os_api': '23',
            'os_version': '6.0.1',
            'uuid': '300000000087236',
            'openudid': '2ca3305f4119dd89',
            'manifest_version_code': '830',
            'resolution': '810*1440',
            'dpi': '270',
            'update_version_code': '8302',
            '_rticket': '1590995035033',
            'mcc_mnc': '46003',
            'ts': '1590995033',
            'app_type': 'normal'
        }

    def get_data(self, **kwargs):
        for i in kwargs:
            self.form[i] = str(kwargs[i])
        return self.form


class RandomTag(object):
    def __init__(self):
        self.nike_name_set = set()
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)

    def get_nickname(self):
        sec_uid = engine.execute("select nickname,id from user_info where is_run=0 limit 1")
        x = sec_uid.fetchall()
        data = jieba.cut(x[0][0], cut_all=True)
        sid = x[0][1]
        for i in data:
            if len(i) > 1:
                try:
                    int(i)
                except ValueError:
                    if not self.r.sismember('nike_name_tag', str(i)) and is_chinese(i):
                        self.nike_name_set.add(i)
                        self.r.sadd('nick_name_tag', i)
        if not self.nike_name_set:
            engine.execute('update user_info set is_run=1 where id=%s' % sid)
            self.get_nickname()
        engine.execute('update user_info set is_run=1 where id=%s' % sid)

    def choice_tag(self):
        if not len(self.nike_name_set):
            self.get_nickname()
        return self.nike_name_set.pop()





