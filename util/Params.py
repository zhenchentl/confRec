#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: Params.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2014年12月12日 星期五 16时46分12秒
#########################################################################

FILE_DIR = '/home/zhenchentl/workspace/confRec/'

PATH_DBLP_XML = FILE_DIR + 'data/dblp.xml'
PATH_CONF_LIST = FILE_DIR + "code/util/datamining_conf_list.txt"

PATH_AUTHOR_DOC = FILE_DIR + "data/authorDocs.txt"
PATH_CONF_DOC = FILE_DIR + "data/confDocs.txt"

PATH_LDA_DIC = FILE_DIR + "data/lda_dic.dict"
PATH_LDA_MM = FILE_DIR + "data/lda_mm.mm"
PATH_LDA_VEC = FILE_DIR + "data/lda_vec_100.txt"

PARAM_TESTING_START = 2012
PARAM_MIN_COAUTHORS = 5
PARAM_TARGETNODE_NUM = 100

PATH_TARGETNODE_LIST = FILE_DIR + "code/util/targetnode_" \
    + str(PARAM_TARGETNODE_NUM) + ".txt"
