#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: util.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2014年12月12日 星期五 17时02分11秒
#########################################################################
import sys
sys.path.append('..')
from util.Params import *
import re
from redisHelper.RedisHelper import RedisHelper
import random
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)
from math import sqrt

'''余弦相似度'''
def sim_distance_cos(p1, p2):
    '''p1和p2是dict的话，遍历会更迅速'''
    c = list(set(p1.keys()) & set(p2.keys()))
    ss = sum([float(p1[i]) * float(p2[i]) for i in c])
    sq1 = sqrt(sum([pow(float(p1[i]), 2) for i in p1]))
    sq2 = sqrt(sum([pow(float(p2[i]), 2) for i in p2]))
    if sq1 * sq2 != 0:
        return float(ss)/(sq1 * sq2)
    return 0.0

def saveTargetNodes():
    ''' 推荐目标条件：
        1，2012年前后在data mining领域都发表过论文。（总共至少两篇）
        2，合作者数目大于等于五人。
        3, 至少有一个会议是在2012年之前没接触过的。
        4, 作者类型分三种：发表论文数>15(大牛)，>8 && <=15（一般），<=8（新手）
    '''
    mRedis = RedisHelper()
    targetNode = list()
    authors  = mRedis.getAllAuthors()
    logging.info(len(authors))
    while True:
        author = random.choice(authors)
        if len(author.split()) < 2:
            # 有些作者名只有一个词啊你妹，这样很容易重名。
            continue
        if len(mRedis.getAuCoauthors(author)) >= PARAM_MIN_COAUTHORS:
            # 目标合作者数目大于等于五人
            times = mRedis.getAuPaperTimes(author)
            if True in [int(time) >= PARAM_TESTING_START for time in times]\
            and True in [int(time) < PARAM_TESTING_START for time in times]\
            and len(times) <= 8 :#（大牛）
                # 2012年前后在data mining领域都发表过论文。（总共至少两篇）
                confs = mRedis.getAuConfs(author)
                for conf in confs:
                    times = mRedis.getPubTimeList(author, conf)
                    # 至少有一个会议是在2012年之前没接触过的。
                    if False not in [int(time) >= PARAM_TESTING_START for time in times]:
                        targetNode.append(author)
                        break
                logging.info(len(set(targetNode)))
                if len(set(targetNode)) == PARAM_TARGETNODE_NUM:
                    break
    with open(PATH_TARGETNODE_LIST, 'w') as fileWriter:
        for node in set(targetNode):
            fileWriter.write(node + '\n')
        fileWriter.close()

def getTargetList():
    targets = list()
    with open(PATH_TARGETNODE_LIST, 'r') as fileReader:
        for line in fileReader:
            targets.append(line.strip())
        fileReader.close()
    return targets

def formateDocs(doc):
    s = re.sub("[^a-zA-Z0-9\-]", " ", doc)
    s = s.lower()
    return s

def getConfList():
    with  open(PATH_CONF_LIST) as fileReader:
        ConfList = fileReader.readline().strip().split(',')
        fileReader.close()
        return ConfList
    return None

if __name__ == '__main__':
    saveTargetNodes()