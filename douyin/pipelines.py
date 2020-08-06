# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/qunong?charset=utf8mb4")
Base = declarative_base()
Base.metadata.create_all(engine)


class UserInfo(Base):
    __tablename__ = 'user_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(32))  # uid
    sec_uid = Column(String(128))  # sec_uid
    nickname = Column(String(32))  # 昵称
    birthday = Column(String(32))  # 生日
    province = Column(String(8))  # 省份
    location = Column(String(8))  # 市
    city = Column(String(8))  # 区
    fans_count = Column(String(8))  # 粉丝数
    following_count = Column(String(8))  # 关注数
    total_favorited = Column(String(128))  # 点赞数
    aweme_count = Column(String(8))  # 视频数量
    avatar_thumb = Column(String(128))  # 头像
    signature = Column(String(128))  # 签名
    classify = Column(String(12))  # 分类
    is_run = Column(Integer(), default=0)  # 是否已爬取


class UserInfoPipeline:
    Session = sessionmaker(bind=engine)
    session = Session()

    def process_item(self, item, spider):
        user_info = UserInfo(
            uid=item["uid"], sec_uid=item["sec_uid"], nickname=item["nickname"],birthday=item["birthday"],
            province=item["province"], location=item["location"], city=item["city"],fans_count=item["fans_count"],
            following_count=item["following_count"], total_favorited=str(item["total_favorited"]),
            aweme_count=item["aweme_count"], avatar_thumb=item["avatar_thumb"],
            signature=item["signature"], classify=item["classify"]
        )
        self.session.add(user_info)
        try:
            self.session.commit()
        except:
            self.session.rollback()
