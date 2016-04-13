#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: graph.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2015年01月05日 星期一 07时14分50秒
#########################################################################
import sys
sys.path.append('..')
import networkx as nx
from util.utils import *
from util.Params import *
from util.utils import *
from redisHelper.RedisHelper import RedisHelper
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)

class Graph():
    def __init__(self):
        self.graph = nx.Graph()
        self.confs = getConfList()

    def getTrainingGraph(self):
        mRedis = RedisHelper()
        for author in mRedis.getAllAuthors():
            for conf in mRedis.getAuConfs(author):
                Bool_Lc = [int(time) < PARAM_TESTING_START \
                          for time in mRedis.getPubTimeList(author,\
                                                               conf)]
                if True in Bool_Lc:
                    self.graph.add_edge(conf, author, \
                                        weight =20 * Bool_Lc.count(True))
            for coau in mRedis.getAuCoauthors(author):
                Bool_La = [int(time) < PARAM_TESTING_START \
                            for time in mRedis.getCoTimeList(author, \
                                                             coau)]
                if True in Bool_La:
                    self.graph.add_edge(coau, author, \
                                        weight = Bool_La.count(True))
#         for node in self.graph.nodes():
#             node_degree = self.graph.degree(node)
#             detas = dict()
#             for coau in self.graph.neighbors(node):
#                 if coau not in self.confs:
#                     detas[coau] = abs(self.graph.degree(coau) - node_degree)
#             if len(detas) != 0:
#                 max_deta = max(detas.values())
#             else:
#                 max_deta = 0
#             for coau in self.graph.neighbors(node):
#                 if coau not in self.confs:
#                     self.graph[coau][node]['weight'] = self.graph[coau][node]['weight'] * (1.0-detas[coau]*1.0/(max_deta+1))
# #                     print self.graph[coau][node]['weight']
        logging.info('load graph done!')
        logging.info('nodes:' + str(self.graph.number_of_nodes()))
        logging.info('edges:' + str(self.graph.number_of_edges()))
        return self.graph

if __name__ == '__main__':
    G = Graph().getTrainingGraph()