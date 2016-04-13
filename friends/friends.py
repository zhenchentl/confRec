#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: friends.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2015年01月08日 星期四 10时45分22秒
#########################################################################
import sys
sys.path.append('..')
from redisHelper.RedisHelper import RedisHelper
from util.Params import *
from operator import itemgetter
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)

class Friends():
    def __init__(self):
        self.confs = dict()

    def getFriendsConfs(self, author, mRedis):
        friends = list()
        for coau in mRedis.getAuCoauthors(author):
            if True in [int(time) < PARAM_TESTING_START \
                        for time in mRedis.getCoTimeList(author, coau)]:
                friends.append(coau)
                for cocoau in mRedis.getAuCoauthors(coau):
                    if True in [int(time) < PARAM_TESTING_START \
                                for time in mRedis.getCoTimeList(coau, cocoau)]:
                        friends.append(cocoau)
        friends = list(set(friends))
        recom_D = dict()
        for friend in friends:
            confs = mRedis.getAuConfs(friend)
            for conf in confs:
                if True in [int(time) < PARAM_TESTING_START \
                        for time in mRedis.getPubTimeList(friend, conf)]:
                    times = mRedis.getPubTimeList(author, conf)
                    if PARAM_IS_RECOM_NEW:
                        # 如果是推荐全新的，则2012年之前合作过的不推荐，相似度置为0.
                        if len(times) == 0 or False not in [time >= PARAM_TESTING_START 
                                                            for time in times]:
                            recom_D[conf] = recom_D.setdefault(conf, 0) + 1
                        else:
                            recom_D[conf] = 0.0
                    else:
                        # 如果是推荐最有价值的，则不管以前是否合作过。
                        recom_D[conf] = recom_D.setdefault(conf, 0) + 1
                else:
                    recom_D[conf] = 0.0
        return sorted(recom_D.iteritems(), key=itemgetter(1), reverse=True)