# -*- coding:utf-8 -*-


# maya
import pymel.core as pm
import maya.cmds as mc

# lego
from lego.core.api import (
    log,
    const,
    prepost
)
from lego.blocks.api import lib

#
import importlib


def ready(context):
    """ Assembly ready
    
    step 0. pre scripts run
    step 1. return network root node

    context : context(dict)

    """

    guide = None
    node = None
    try:
        guide = pm.selected(type="transform")[0]
        node = guide.message.connections()[0]
    except:
        raise Exception("guide : {0}, nodes : {1}".format(guide, node))
    
    if node.hasAttr(const.ISLEGO):
        pre = node.attr(const.PRESCRIPTS).get().split(const.SEPARATOR)
    else:
        pre = None
    
    for script in pre:
        mod = importlib.import_module(script)
        mod.PrePost.run(context)

    return node.name()

def stacking_blocks(context, node):
    """ Assemble blocks

    step 0. get block info
    step 1. stacking block 
    step 2. stacking_blocks(context, childnode)

    context : context(dict)
    node : network node(str)

    """

    info = get_block_info(node)
    children = info[const.CHILDREN]
    if not children:
        return False
    
    if const.WORLD not in context:
        lib.world(context)

    if info[const.KIND] == const.COMPONENT:
        for child in children:
            context[child] = dict()
            lib.stacking_block(context[child], child)
        
    for child in children:
        stacking_blocks(context, child)
        

def clear(context, node):
    """ Clear scene 

    step 0. rig clean up
    step 1. post script run
    
    context : context(dict)
    node : network root node(str)

    """
    context["mesh"]
    context["joints"]
    context["controllers"]

    node = pm.PyNode(node)
    if node.hasAttr(const.ISLEGO):
        pre = node.attr(const.POSTSCRIPTS).get().split(const.SEPARATOR)
    else:
        pre = None
    
    for script in pre:
        mod = importlib.import_module(script)
        mod.PrePost.run(context)

def get_block_info(node):
    """ get block info 

    """
    node = pm.PyNode(node)
    info = dict()

    info[const.KIND]                = node.attr(const.KIND).get()

    info[const.BLOCK_TYPE]          = node.attr(const.BLOCK_TYPE).get()
    info[const.BLOCK_VERSION]       = node.attr(const.BLOCK_VERSION).get()
    info[const.BLOCK_NAME]          = node.attr(const.BLOCK_NAME).get()
    info[const.BLOCK_INDEX]         = node.attr(const.BLOCK_INDEX).get()
    info[const.BLOCK_SIDE]          = node.attr(const.BLOCK_SIDE).get()
    info[const.BLOCK_FEATURE]       = node.attr(const.BLOCK_FEATURE).connections()
    info[const.BLOCK_UI]            = node.attr(const.BLOCK_UI).get()

    info[const.BLOCK_PARENT]        = node.attr(const.BLOCK_PARENT).get()
    info[const.BLOCK_PARENT_SPACE]  = node.attr(const.BLOCK_PARENT_SPACE).get()

    info[const.CHILDREN]            = node.attr(const.CHILDREN).connections()
    info[const.INPUT]               = node.attr(const.INPUT).get()
    info[const.OUTPUT]              = node.attr(const.OUTPUT).get().split(const.SEPARATOR)
    info[const.PRESCRIPTS]          = node.attr(const.PRESCRIPTS).get().split(const.SEPARATOR)
    info[const.POSTSCRIPTS]         = node.attr(const.POSTSCRIPTS).get().split(const.SEPARATOR)
    

    return info
