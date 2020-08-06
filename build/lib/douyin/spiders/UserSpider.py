# -*- coding: utf-8 -*-
from abc import ABCMeta

import scrapy
import json
from douyin.DevicesData import DeviceConfig, UserConfig
from douyin.items import DouyinUserInfoItem
from douyin.tools import RequestsStructure, FormStructure
from douyin.tools import RandomTag


class UserInfoSpider(scrapy.Spider, metaclass=ABCMeta):
    name = 'userinfo'
    allowed_domains = []
    device_data = DeviceConfig.xiaomi
    random_tag = RandomTag()
    cursor = 0
    tag = ''

    def start_requests(self):
        form_structure = FormStructure()
        """ spider启动执行，只会执行者一次 """
        urls = "https://aweme.snssdk.com/aweme/v1/discover/search/?" + self.device_data
        requests_structure = RequestsStructure(self.device_data, cookies=UserConfig.cookie,
                                               x_tt_token=UserConfig.x_tt_token)
        header = requests_structure.get_header()
        self.tag = self.random_tag.choice_tag()
        formdata = form_structure.get_data(
            keyword="os", cursor=self.cursor, count=10, type=1, is_pull_refresh=1, hot_search=0,
            search_source='', search_id='', query_correct_type=1
        )
        yield scrapy.FormRequest(url=urls, headers=header, formdata=formdata, callback=self.parse_sec_id)

    def parse_sec_id(self, response):
        form_structure = FormStructure()
        response_json = json.loads(response.text, encoding='utf-8')
        user_info = response_json['user_list']
        if not user_info:
            self.tag = self.random_tag.choice_tag()
            self.cursor = 0
        for i in user_info:
            sec_uid = i['user_info']['sec_uid']
            formdata = form_structure.get_data(sec_user_id=sec_uid)
            from urllib import parse
            params1 = parse.urlencode(formdata)
            requests_structure = RequestsStructure(params=params1,
                                                   cookies=UserConfig.cookie, x_tt_token=UserConfig.x_tt_token)
            headers = requests_structure.get_header()
            urls = 'https://aweme-eagle.snssdk.com/aweme/v1/user/?' + params1
            yield scrapy.Request(url=urls, headers=headers, body=params1, callback=self.parse_user_info,)

        urls = "https://aweme.snssdk.com/aweme/v1/discover/search/?" + self.device_data
        self.cursor += len(user_info)
        requests_structure = RequestsStructure(self.device_data, cookies=UserConfig.cookie,
                                               x_tt_token=UserConfig.x_tt_token)
        header = requests_structure.get_header()
        formdata = form_structure.get_data(
            keyword=self.tag, cursor=self.cursor, count=10, type=1, is_pull_refresh=1, hot_search=0,
            search_source='', search_id='', query_correct_type=1
        )
        print("当前右游标位置:%d， 当前关键词:%s" % (self.cursor, self.tag))
        yield scrapy.FormRequest(url=urls, headers=header, formdata=formdata,
                                 callback=self.parse_sec_id)

    def parse_user_info(self, response):
        """ 进入到用户信息页面，解析用户的数据 """
        user_info_item = DouyinUserInfoItem()
        response_json = json.loads(response.text, encoding='utf-8')
        user_info_data = response_json['user']

        if user_info_data['uid']:
            user_info_item['uid'] = str(user_info_data['uid'])  # uid
        user_info_item['sec_uid'] = user_info_data['sec_uid']  # sec_uid
        user_info_item['nickname'] = user_info_data['nickname']  # 昵称

        user_info_item['province'] = 'null'
        if user_info_data['province']:
            user_info_item['province'] = user_info_data['province']

        # 检查生日数据是否存在
        user_info_item['birthday'] = 'null'  # 生日
        if user_info_data['birthday']:
            user_info_item['birthday'] = user_info_data['birthday']

        user_info_item['city'] = 'null'
        if user_info_data['city']:
            user_info_item['city'] = user_info_data['city']

        user_info_item['location'] = 'null'
        if str(user_info_data['hide_location']) != 'True':
            user_info_item['location'] = user_info_data['location']

        user_info_item['fans_count'] = str(user_info_data['mplatform_followers_count'])  # 粉丝数

        user_info_item['following_count'] = str(user_info_data['following_count'])  # 关注数

        user_info_item['total_favorited'] = str(user_info_data['total_favorited'])  # 点赞数

        user_info_item['aweme_count'] = str(user_info_data['aweme_count'])  # 视频数量

        user_info_item['avatar_thumb'] = user_info_data['avatar_thumb']["url_list"][0]  # 头像

        user_info_item['classify'] = self.tag

        user_info_item['signature'] = 'null'
        if user_info_data['signature']:
            user_info_item['signature'] = user_info_data['signature']  # 签名
        yield user_info_item


if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute("scrapy crawl userinfo".split())