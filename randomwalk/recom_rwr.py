#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: recom_rwr.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2015年01月07日 星期三 20时20分07秒
#########################################################################
import sys
from randomwalk.pagerank import RandomWalk
from redisHelper.RedisHelper import RedisHelper
from operator import itemgetter
sys.path.append('..')
from graph import Graph
from util.utils import *
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)

def recommender():
    graph = Graph().getTrainingGraph()
    targets = getTargetList()
    mRedis = RedisHelper()
    recom_dict = dict()
    confs = mRedis.getAllConfs()
    rw = RandomWalk()
    for index, author in enumerate(targets):
        logging.info(str(index))
        pagerank = rw.PageRank(graph, author)
#         print sorted(pagerank.iteritems(), key=itemgetter(1), reverse=True)[0:200]
        recom_dict[author] = getReomList(pagerank, confs, author, mRedis)
    saveRecomList(recom_dict)

def getReomList(pagerank, confs, author, mRedis):
    recom_D = dict()
    for conf in confs:
        times = mRedis.getPubTimeList(author, conf)
        if PARAM_IS_RECOM_NEW:
            # 如果是推荐全新的，则2012年之前合作过的不推荐，相似度置为0.
            if len(times) == 0 or False not in [time >= PARAM_TESTING_START 
                                                for time in times]:
                recom_D[conf] = pagerank[conf]
            else:
                recom_D[conf] = 0.0
        else:
            # 如果是推荐最有价值的，则不管以前是否合作过。
            recom_D[conf] = pagerank[conf]
    return sorted(recom_D.iteritems(), key=itemgetter(1), reverse=True)

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