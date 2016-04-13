#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: recom_lda.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2015年01月03日 星期六 16时09分52秒
#########################################################################
import sys
sys.path.append('..')
from util.Params import *
from util.utils import *
from redisHelper.RedisHelper import RedisHelper
from operator import itemgetter
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)

def RecomConfForAuthor(mRedis, author):
    sim = dict()
    authorVec = mRedis.getAuthorVec(author)
    for conf in mRedis.getAllConfs():
        times = mRedis.getPubTimeList(author, conf)
        if PARAM_IS_RECOM_NEW:
            # 如果是推荐全新的，则2012年之前合作过的不推荐，相似度置为0.
            if len(times) == 0 or False not in [time >= PARAM_TESTING_START 
                                                for time in times]:
                confVec = mRedis.getConfVec(conf)
                sim[conf] = sim_distance_cos(authorVec, confVec)
            else:
                sim[conf] = 0.0
        else:
            # 如果是推荐最有价值的，则不管以前是否合作过。
            confVec = mRedis.getConfVec(conf)
            sim[conf] = sim_distance_cos(authorVec, confVec)
    recom_list = sorted(sim.iteritems(), key = itemgetter(1), \
                  reverse = True)
    sim = {}
    return recom_list

def recommender():
    mRedis = RedisHelper()
    recom_dict = dict()
    targetNodes = getTargetList()
    index = 0
    for author in targetNodes:
        index += 1
        logging.info(author + ':' + str(index))
        recom_dict[author] = RecomConfForAuthor(mRedis, author)
    saveRecomList(recom_dict)

def saveRecomList(recom_dict):
    '''
    recom dict保存格式：author-->conf1:sim,conf2:sim,conf3:sim...
    '''
    with open(PATH_RECOM_LIST,'w') as file_input:
        for tg in recom_dict:
            recom_str = ','.join([conf + ':' + str(sim) \
                                  for conf, sim in recom_dict[tg]])
            file_input.write(tg + '-->' + recom_str + '\n')
        file_input.close()

if __name__ == '__main__':
    recommender()