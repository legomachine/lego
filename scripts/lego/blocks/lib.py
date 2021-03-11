# -*- coding:utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

def get_node_name(rule, description="", extension=""):
    name = rule.format(description=description, extension=extension)
    split_name = [x for x in name.split("_") if not x]
    return "_".join(split_name)

def get_joint_name():
    pass
