#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: performanceSOI.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2015年01月08日 星期四 08时36分01秒
#########################################################################
import sys
sys.path.append('..')
from util.Params import *
from util.utils import *
import math
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

def getConfSOI():
    confSOI = dict()
    with open(PAHT_CONF_SOI, 'r') as fileReader:
        for line in fileReader:
            conf = line.strip().split(',')
            if len(conf) < 2:
                confSOI[conf[0]] = 0
            else:
                confSOI[conf[0]] = int(conf[1])
        fileReader.close()
    avg = sum(confSOI.values())/ len(confSOI)
    for key in confSOI.keys():
        if confSOI[key] == 0:
            confSOI[key] = avg
    return confSOI

if __name__ == '__main__':
    RecomConfDict = getRecomConf()
    confSOI = getConfSOI()
    for recomNum in range(1, 74, 2):
        soi,count = 0,0
        for author in RecomConfDict.keys():
            soi += sum([confSOI[conf] for conf in RecomConfDict[author][:recomNum]])
            count += recomNum
        print recomNum,soi * 1.0 / count
            