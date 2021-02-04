# -*- coding:utf-8 -*-

def log(level, msg):
    """ 

    level 0 : info
    level 1 : warning
    level 2 : error

    """

    dent = "    "
    print(dent * level + msg)