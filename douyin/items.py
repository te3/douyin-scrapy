# -*- coding: utf-8 -*-

import scrapy


class DouyinUserInfoItem(scrapy.Item):
    # define the fields for your item here like:
    uid = scrapy.Field()  # uid
    sec_uid = scrapy.Field()  # sec_uid
    nickname = scrapy.Field()  # 昵称
    birthday = scrapy.Field()  # 生日
    province = scrapy.Field()  # 省份
    location = scrapy.Field()  # 市
    city = scrapy.Field()  # 区
    fans_count = scrapy.Field()  # 粉丝数
    following_count = scrapy.Field()  # 关注数
    total_favorited = scrapy.Field()  # 点赞数
    aweme_count = scrapy.Field()  # 视频数量
    avatar_thumb = scrapy.Field()  # 头像
    signature = scrapy.Field()  # 签名
    classify = scrapy.Field()  # 分类
