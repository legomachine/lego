# -*- coding:utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

# maya
import pymel.core as pm

# lego
from lego.core.api import (
    log,
    const,
    prepost
)

#
import importlib


def ready(context):
    """ Assembly ready
    
    step 0. pre scripts run
    step 1. return network root node

    context : context(dict)

    """
    log.log(level=0, msg="ready !")
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

    if const.INIT not in context:
        init_rig_hierarchy(context, node)
    info = get_block_info(node)
    context_name = "{0}_{1}{2}".format(info[const.BLOCK_NAME], info[const.BLOCK_NAME], info[const.BLOCK_NAME])
    naming_rule = info[const.NAMERULE].format(info[const.BLOCK_NAME],
                                              info[const.BLOCK_NAME],
                                              info[const.BLOCK_NAME],
                                              "{description}",
                                              "{extension}")
    if context_name not in context:
        context[context_name] = dict()
        context[context_name][const.NAMERULE] = naming_rule

    if not info[const.ISLEGO]:
        block = importlib.import_module("lego.blocks.legobox.{0}".format(info[const.BLOCK_TYPE]))

        if const.STEP not in context[context_name]:
            block.build(context[context_name], node, 0)
            context[context_name][const.STEP] = 1
        elif context[context_name][const.STEP] == 1:
            block.build(context[context_name], node, 1)
            context[context_name][const.STEP] = 2
        else:
            block.build(context[context_name], node, 2)

    if info[const.CHILDREN]:
        for child in info[const.CHILDREN]:
            stacking_blocks(context, child)
    else:
        return True

def clear(context, node):
    """ Clear scene 

    step 0. rig clean up
    step 1. post script run
    
    context : context(dict)
    node : network root node(str)

    """

    log.log(level=0, msg="clear !".format(node.attr(const.BLOCK_TYPE).get()))
    node = pm.PyNode(node)
    info = get_block_info(node)
    
    for script in info[const.POSTSCRIPTS]:
        mod = importlib.import_module(script)
        mod.PrePost.run(context)

def init_rig_hierarchy(context, node):
    """ create rig hierarchy 
    rig (hierarchy)
        model
        ---modeling...
        blocks
        ---another blocks...
        joints
        ---binding joints...

    context["init"]["rig"] = root
    context["init"]["model"] = model
    context["init"]["blocks"] = blocks
    context["init"]["joints"] = joints

    """
    log.log(level=0, msg="init hierarchy !")
    origin = dt.Vector(0, 0, 0)
    origin_matrix = transform.getTransformFromPos(origin)

    # node
    rig = primitive.addTransform(None, "rig", m=origin_matrix)
    model = primitive.addTransform(rig, "model", m=origin_matrix)
    blocks = primitive.addTransform(rig, "blocks", m=origin_matrix)
    joints = primitive.addTransform(rig, "joints", m=origin_matrix)

    # connections
    rig.controllersVis >> blocks.v
    rig.jointsVis >> joints.v
    rig.ControllersOnPlaybackVis >> blocks.hideOnPlayback

    # attribute
    attribute.lockAttribute(rig)
    attribute.lockAttribute(model)
    attribute.lockAttribute(blocks)
    attribute.lockAttribute(joints)
    attribute.addAttribute(rig, "controllerVis", "boolean", True)
    attribute.addAttribute(rig, "ControllersOnPlaybackVis", "boolean", False)
    attribute.addAttribute(rig, "jointsVis", "boolean", False)

    context[const.INIT] = dict()
    context[const.INIT]["rig"] = rig
    context[const.INIT]["model"] = model
    context[const.INIT]["blocks"] = blocks
    context[const.INIT]["joints"] = joints

def get_block_info(node):
    """ get block info 

    """
    info = dict()

    info[const.ISROOT]              = node.hasAttr(const.ISLEGO)
    info[const.BLOCK_TYPE]          = node.attr(const.BLOCK_TYPE).get()
    info[const.BLOCK_VERSION]       = node.attr(const.BLOCK_VERSION).get()
    info[const.BLOCK_NAME]          = node.attr(const.BLOCK_NAME).get()
    info[const.BLOCK_SIDE]          = node.attr(const.BLOCK_SIDE).get()
    info[const.BLOCK_INDEX]         = node.attr(const.BLOCK_INDEX).get()
    info[const.BLOCK_FEATURE]       = [x.name.get() for x in node.attr(const.BLOCK_FEATURE).outputs()]
    info[const.BLOCK_UI]            = node.attr(const.BLOCK_UI).get()

    info[const.BLOCK_PARENT]        = node.attr(const.BLOCK_PARENT).get()
    info[const.BLOCK_PARENT_SPACE]  = [x.get() for x in node.attr(const.BLOCK_PARENT_SPACE).inputs(plugins=True)]

    info[const.CHILDREN]            = node.attr(const.CHILDREN).outputs()
    info[const.INPUT]               = node.attr(const.INPUT).get()
    info[const.OUTPUT]              = [x.get() for x in node.attr(const.OUTPUT) if x.get()]
    info[const.PRESCRIPTS]          = [x.get() for x in node.attr(const.PRESCRIPTS) if x.get()]
    info[const.POSTSCRIPTS]         = [x.get() for x in node.attr(const.POSTSCRIPTS) if x.get()]
    
    return info
