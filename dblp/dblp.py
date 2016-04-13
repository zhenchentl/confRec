#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: dblp.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2014年12月12日 星期五 17时00分26秒
#########################################################################

import sys
from redisHelper.RedisHelper import RedisHelper
from pydoc import Doc, doc
sys.path.append('..')
from xml.sax import handler, make_parser
from util.Params import *
from util.utils import *
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)

paperTag = ('article','inproceedings','proceedings','book',
        'incollection','phdthesis','mastersthesis','www')

class dblpHandler(handler.ContentHandler):
    def __init__(self):
        self.mRedis = RedisHelper()
        
        self.isPaperTag = False
        self.conf = ''

        self.isTitleTag = False
        self.titlesDict = dict()
        self.currentID = 0

        self.isAuthorTag = False
        self.authors = list()

        self.isYearTag = False
        self.year = 1970

        self.authorTitleIDs = dict()
        self.confTitleIDs = dict()
        
        self.ConfList = getConfList()

    def startDocument(self):
        logging.info("Document Start...")

    def endDocument(self):
#         saveArticleToDisk(self.mRedis, self.authorTitleIDs, \
#                           self.confTitleIDs, self.titlesDict)
        logging.info("Document End...")

    def startElement(self, name, attrs):
        if name in paperTag:
            self.conf = attrs.get('key').split('/')[1]
            if self.conf in self.ConfList:
                self.isPaperTag = True
        if self.isPaperTag:
            if name == 'title':
                self.isTitleTag = True
            if name == 'author':
                self.isAuthorTag = True
            if name == 'year':
                self.isYearTag = True

    def endElement(self, name):
        if name in paperTag:
            if self.isPaperTag:
                self.isPaperTag = False
                self.mRedis.addItem(self.authors, self.conf, self.year)
#                 cTitleIDs = self.confTitleIDs.setdefault(self.conf,[])
#                 cTitleIDs.append(self.currentID)
#                 for author in self.authors:
#                     aTitleIDs = self.authorTitleIDs.setdefault(author,[])
#                     aTitleIDs.append(self.currentID)
                self.authors = []
                self.conf = ''
                self.year = ''

    def characters(self, content):
        if self.isTitleTag:
            self.currentID = len(self.titlesDict)
            self.titlesDict[self.currentID] = formateDocs(content)
            self.isTitleTag = False
            if self.currentID % 100 == 0:
                logging.info(self.currentID)
        if self.isYearTag:
            self.year = content
            self.isYearTag = False
        if self.isAuthorTag:
            self.authors.append(content)
            self.isAuthorTag = False

def getConfList():
    with  open(PATH_CONF_LIST) as fileReader:
        ConfList = fileReader.readline().strip().split(',')
        fileReader.close()
        return ConfList
    return None

def saveArticleToDisk(mRedis, authorTitleIDs, confTitleIDs, titlesDict):
    with open(PATH_AUTHOR_DOC, 'w') as authorDocWriter:
        docID = 0
        for author, titleIDs in authorTitleIDs.items():
            doc = ' '.join([titlesDict[titleID] \
                            for titleID in titleIDs]) + '\n'
            mRedis.addAuthorDocID(author, docID)
            docID += 1
            authorDocWriter.write(doc)
        authorDocWriter.close()
    with open(PATH_CONF_DOC, 'w') as confDocWriter:
        docID = 0
        for conf, titleIDs in confTitleIDs.items():
            doc = ' '.join([titlesDict[titleID] \
                            for titleID in titleIDs]) + '\n'
            mRedis.addConfDocID(conf, docID)
            docID += 1
            confDocWriter.write(doc)
        confDocWriter.close()

def parserDblpXml():
    handler = dblpHandler()
    parser = make_parser()
    parser.setContentHandler(handler)
    f = open(PATH_DBLP_XML, 'r')
    parser.parse(f)
    f.close()

if __name__ == '__main__':
    parserDblpXml()