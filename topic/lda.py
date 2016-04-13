#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: lda.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2014年12月14日 星期日 11时07分12秒
#########################################################################

from util.Params import *
import logging
from gensim import corpora, models
from redisHelper.RedisHelper import RedisHelper

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)

class baseLda:
    def __init__(self):
        self.mRedis = RedisHelper()
        self.authorDocEnd = -1
        self.docs = list()
        self.corpus_lda = list()
        for line in open(PATH_AUTHOR_DOC, 'r'):
            self.docs.append(line.split())
            self.authorDocEnd += 1
        for line in open(PATH_CONF_DOCNF_DOC, 'r'):
            self.docs.append(line.split())
        print len(self.docs)

    def lda_setp1(self):
        '''Step1'''
        dictionary = corpora.Dictionary(self.docs)
        logging.info("store the dictionary, for future reference.")
        dictionary.save_as_text(PATH_LDA_DIC)
        corpus = [dictionary.doc2bow(doc) for doc in self.docs]
        logging.info("store to disk, for later use.")
        corpora.MmCorpus.serialize(PATH_LDA_MM, corpus)

    def lda_step2(self):
        '''Step2'''
        logging.info("load Dictionary.")
        id2word = corpora.Dictionary.load_from_text(PATH_LDA_DIC)
        logging.info("load corpus iterator.")
        mm = corpora.MmCorpus(PATH_LDA_MM)
        logging.info('LDA Start.')
        lda = models.ldamodel.LdaModel(corpus=mm, id2word=id2word, \
            num_topics=100, update_every=1, chunksize=10000, passes=1)
        logging.info('LDA End')
        self.corpus_lda = list(lda[mm])
        self.saveVec(self.corpus_lda)

    def saveVec(self):
        authors = self.mRedis.getAllAuthors()
        confs = self.mRedis.getAllConfs()
        for author in authors:
            DocId = int(self.mRedis.getDocIdByAuthor(author))
            vec = self.corpus_lda[DocId]
            for topic, value in vec:
                self.mRedis.addAuthorVec(author, \
                                         str(topic) + ':' + str(value))
        for conf in confs:
            DocId = int(self.mRedis.getDocIdByConf(conf))
            vec = self.corpus_lda[DocId + self.authorDocEnd + 1]
            for topic, value in vec:
                self.mRedis.addConfVec(conf, \
                                       str(topic) + ':' + str(value))
        self.docs = []
        self.corpus_lda = []

if __name__ == '__main__':
    baselda = baseLda()
#     baselda.lda_setp1()
    baselda.lda_step2()
