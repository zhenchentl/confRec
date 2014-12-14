#!/usr/bin/env python
#coding=utf-8
#########################################################################
# File Name: util.py
# Author: Mark Chen
# mail: zhenchentl@gmail.com
# Created Time: 2014年12月12日 星期五 17时02分11秒
#########################################################################

import re

def formateDocs(doc):
    s = re.sub("[^a-zA-Z0-9\-]", " ", doc)
    s = s.lower()
    return s