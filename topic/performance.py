#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: performance.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2015年01月03日 星期六 21时18分17秒
#########################################################################
import sys
sys.path.append('..')
from util.Params import *
from util.utils import *
from redisHelper.RedisHelper import RedisHelper

def getRecomConf():
    recomDict = dict()
    with open(PATH_RECOM_LIST, 'r') as fileReader:
        for line in fileReader:
            recomStr = line.split('-->')
            author = recomStr[0]
            recomL = recomDict.setdefault(author,[])
            for confSim in recomStr[1].split(','):
                recomL.append(confSim.split(':')[0])
        fileReader.close()
    return recomDict

def getRelatedConf():
    targetNodes = getTargetList()
    mRedis = RedisHelper()
    relatedConfDict = dict()
    for author in targetNodes:
        confs = mRedis.getAuConfs(author)
        relatedL = relatedConfDict.setdefault(author, [])
        for conf in confs:
            times = mRedis.getPubTimeList(author, conf)
            if PARAM_IS_RECOM_NEW:
                # 推荐全新的会议，之前没有参加过，2012年后参加了。
                if False not in [int(time) >= PARAM_TESTING_START for time in times]:
                    relatedL.append(conf)
            else:
                # 推荐最有价值的会议，可能之前参加过，2012年后参加了。
                if True in [int(time) >= PARAM_TESTING_START for time in times]:
                    relatedL.append(conf)
    return relatedConfDict

if __name__ == '__main__':
    RecomConfDict = getRecomConf()
    RelatedConfDict = getRelatedConf()
    for recomNum in range(1, 74, 2):
        precision, recall = 0.0, 0.0
        for author in RecomConfDict.keys():
            hit = len(set(RecomConfDict[author][0:recomNum]) & \
                      set(RelatedConfDict[author]))
            precision += hit * 1.0 / recomNum
            recall += hit * 1.0 / len(RelatedConfDict[author])
        precision /= len(RecomConfDict.keys())
        recall /= len(RecomConfDict.keys())
#         print precision
#         print 0.0 if (precision + recall) == 0 \
#                    else 2.0 * precision * recall/(precision + recall)
        print precision, recall, 0.0 if (precision + recall) == 0 \
                  else 2.0 * precision * recall/(precision + recall)
                   