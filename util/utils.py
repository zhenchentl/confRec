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

def saveTargetNodes():
    ''' 推荐目标条件：
        1，2012年前后在data mining领域都发表过论文。（总共至少两篇）
        2，合作者数目大于等于五人。
    '''
    mRedis = RedisHelper()
    targetNode = list()
    authors  = mRedis.getAllAuthors()
    logging.info(len(authors))
    while True:
        author = random.choice(authors)
        if len(mRedis.getAuCoauthors(author)) >= PARAM_MIN_COAUTHORS:
            times = mRedis.getAuPaperTimes(author)
            if True in [int(time) >= PARAM_TESTING_START for time in times]\
            and True in [int(time) < PARAM_TESTING_START for time in times]:
                targetNode.append(author)
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
            targets.append(line)
        fileReader.close()
    return targets

def formateDocs(doc):
    s = re.sub("[^a-zA-Z0-9\-]", " ", doc)
    s = s.lower()
    return s

if __name__ == '__main__':
    saveTargetNodes()