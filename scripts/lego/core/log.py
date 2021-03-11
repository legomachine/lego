# -*- coding:utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

def log(level, msg):
    """ 

    level 0 : info
    level 1 : warning
    level 2 : error

    msg : message(str)
    
    """

    dent = "    "
    print(dent * level + msg)