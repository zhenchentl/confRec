#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: RedisHelper.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2014年12月12日 星期五 16时51分24秒
#########################################################################

import redis
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)

IP = '127.0.0.1'
PORT = 6379

'''key-->set：学者的所有合作者。author-->(coau1, coau2, coau3...)'''
DB_AU_COAU_SET = 0
'''key-->set：学者参加的会议。author-->(conf1, conf2,conf3...)'''
DB_AU_CONF_SET = 1
'''key-->set：会议中所有学者。conf-->(author1, author2, author3...)'''
DB_CONF_AU_SET = 2
'''key-->set：两个人合作的所有论文时间。author:author-->(time1, time2, time3...)'''
DB_AU_AU_TIME_SET = 3
'''key-->set：学者在某会议上发表所有论文时间。author:conf-->(time1, time2, time3...)'''
DB_AU_CONF_TIME_SET = 4
'''key-->value：学者对应的文档ID。author-->docID'''
DB_AU_DOCID = 5
'''key-->value：会议对应的文档ID。conf-->docID'''
DB_CONF_DOCID = 6
'''key-->set：学者对应的特征向量（LDA）。author-->(value1, value2, value3...)'''
DB_AU_VEC_SET = 7
'''key-->set：会议对应的特征向量（LDA）。conf-->(value1, value2, value3...)'''
DB_CONF_VEC_SET = 8

class RedisHelper:
    def __init__(self):
        try:
            self.AuCoauSet = redis.StrictRedis(IP, port = PORT, db = DB_AU_COAU_SET)
            self.AuConfSet = redis.StrictRedis(IP, port = PORT, db = DB_AU_CONF_SET)
            self.ConfAuSet = redis.StrictRedis(IP, port = PORT, db = DB_CONF_AU_SET)
            self.AuAuTimeSet = redis.StrictRedis(IP, port = PORT, db = DB_AU_AU_TIME_SET)
            self.AuConfTimeSet = redis.StrictRedis(IP, port = PORT, db = DB_AU_CONF_TIME_SET)
            self.AuDocID = redis.StrictRedis(IP, port = PORT, db = DB_AU_DOCID)
            self.ConfDocID = redis.StrictRedis(IP, port = PORT, db = DB_CONF_DOCID)
            self.AuVecSet = redis.StrictRedis(IP, port = PORT, db = DB_AU_VEC_SET)
            self.ConfVecSet = redis.StrictRedis(IP, port = PORT, db = DB_CONF_VEC_SET)
        except:
            logging.info("can not open Redis database")
            
    def addItem(self, authors, conf, year):
        for au in authors:
            self.addAuConf(au, conf, year)
            for coau in authors:
                if au != coau:
                    self.addAuCoauthor(au, coau, year)

    def addAuCoauthor(self, author, coauthor, year):
        self.AuCoauSet.sadd(author, coauthor)
        self.AuAuTimeSet.sadd(author + ':' + coauthor, year)

    def addAuConf(self, author, conf, year):
        self.ConfAuSet.sadd(conf, author)
        self.AuConfSet.sadd(author, conf)
        self.AuConfTimeSet.sadd(author + ':' + conf, year)

    def addAuthorDocID(self, author, docID):
        self.AuDocID.set(author, docID)

    def addConfDocID(self, conf, docID):
        self.ConfDocID.set(conf, docID)

    def addAuthorVec(self, author, VecItem):
        self.AuVecSet.sadd(author, VecItem)

    def addConfVec(self, conf, VecItem):
        self.ConfVecSet.sadd(conf, VecItem)

    def getAllAuthors(self):
        return self.AuDocID.keys()

    def getAllConfs(self):
        return self.ConfDocID.keys()

    def getDocIdByAuthor(self, author):
        return self.AuDocID.get(author)

    def getDocIdByConf(self, conf):
        return self.ConfDocID.get(conf)

    def getAuCoauthors(self, author):
        return self.AuCoauSet.smembers(author)
    
    def getAuConfs(self, author):
        return self.AuConfSet.smembers(author)
    
    def getConfAuthors(self, conf):
        return self.ConfAuSet.smembers(conf)

    def getCoTimeList(self, author, coauthor):
        return self.AuAuTimeSet.smembers(author + ':' + coauthor)

    def getPubTimeList(self, author, conf):
        return self.AuConfTimeSet.smembers(author + ':' + conf)

    