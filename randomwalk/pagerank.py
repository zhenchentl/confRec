#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: pagerank.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2015年01月05日 星期一 07时11分36秒
#########################################################################
import sys
sys.path.append('..')
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)

class RandomWalk():
    def __init__(self):
        self.S = dict()

    def PageRank(self, graph, current_node='Tingting He', damping_factor=0.95,\
            max_iterations=20, min_delta=0.0001):
        """
        Compute and return the PageRank in an directed graph.
        @type  graph: digraph
        @param graph: Digraph.
        @type  damping_factor: number
        @param damping_factor: PageRank dumping factor.
        @type  max_iterations: number
        @param max_iterations: Maximum number of iterations.
        @type  min_delta: number
        @param min_delta: Smallest variation required for a new iteration.
        @rtype:  Dict
        @return: Dict containing all the nodes PageRank.
        """
        nodes = graph.nodes()
        graph_size = graph.number_of_nodes()
        '''if the random walk start from one node,set the rank as 1.0,while others 0'''
        pagerank = dict.fromkeys(nodes, 0)
        pagerank[current_node] = 1.0
        min_value = damping_factor / graph_size
        for i in range(max_iterations):
            diff = 0
            for node in nodes:
                rank = min_value
                for referring_page in graph.neighbors(node):
#                     rank += damping_factor * pagerank[referring_page] / \
#                         graph.degree(referring_page)
                    rank += damping_factor * pagerank[referring_page] * \
                        self.Trans(graph, node, referring_page)
                diff += abs(pagerank[node] - rank)
                pagerank[node] = rank
            '''重启动概率'''
            pagerank[current_node] += 1-damping_factor
            '''stop if PageRank has converged'''
            if diff < min_delta:
                break
        logging.info('itertimes:' + str(i))
        return pagerank
    
    def Trans(self, graph,node, referring_page):
        if self.S.setdefault(referring_page+':'+node, 0) == 0:
            self.S[referring_page+':'+node] = 1.0 / graph.degree(referring_page)
#             self.S[referring_page+':'+node] = graph[node][referring_page]['weight'] * 1.0/ \
#             sum([graph[tmp][referring_page]['weight'] \
#                  for tmp in graph.neighbors(referring_page)])
#         print self.S[referring_page+':'+node]
        return self.S[referring_page+':'+node]