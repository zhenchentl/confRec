#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: recom_frie.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2015年01月08日 星期四 12时07分04秒
#########################################################################

import sys
sys.path.append('..')
from redisHelper.RedisHelper import RedisHelper
from friends import Friends
from util.utils import *
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)

def recommender():
    targets = getTargetList()
    mRedis = RedisHelper()
    recom_dict = dict()
    for index, author in enumerate(targets):
        logging.info(str(index))
        recom_D = Friends().getFriendsConfs(author, mRedis)
        recom_dict[author] = recom_D
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