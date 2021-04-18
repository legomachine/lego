# -*- coding:utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

# mgear
from mgear.core import node, fcurve, applyop, vector, icon
from mgear.core import attribute, transform, primitive

# maya
import pymel.core as pm
import pymel.core.datatypes as dt

# lego
from lego.core.api import (
    log,
    const,
    prepost
)
from lego.blocks import lib

#
import importlib
import pprint
from collections import OrderedDict



def ready(context):
    """ Assembly ready
    
    step 0. pre scripts run
    step 1. return network root node

    context : context(dict)

    """
    log.log(level=0, msg="ready !")
    guide = None
    network = None
    try:
        guide = pm.selected(type="transform")[0]
        network = guide.message.connections()[0]
    except:
        raise Exception("guide : {0}, network : {1}".format(guide, network))
    
    if network.hasAttr(const.ISLEGO):
        pre = network.attr(const.PRESCRIPTS).get()
    else:
        pre = list()
    
    for script in pre:
        mod = importlib.import_module(script)
        mod.PrePost.run(context)

    # naming
    root_guide = guide.getParent(generations=-1)
    root_network = root_guide.message.outputs(type="network")[0]
    common_name = root_network.attr(const.COMMONNAME).get()
    joint_name = root_network.attr(const.JOINTNAME).get()
    side_name = map(lambda x: str() if x is None else x, root_network.attr(const.SIDENAME).get())
    con_exp = root_network.attr(const.CONEXP).get()
    jnt_exp = root_network.attr(const.JNTEXP).get()

    context[const.NAMING] = (common_name, joint_name, side_name, con_exp, jnt_exp)

    return network

def blocks_list(network, blocks):
    children = network.attr(const.CHILDREN).outputs(type="network")
    if children:
        blocks.extend(children)
        for child in children:
            blocks_list(child, blocks)
    else:
        return

def stacking_blocks(context, network):
    """ Assemble blocks

    step 0. get block info
    step 1. stacking block 
    step 2. stacking_blocks(context, childnode)

    context : context(dict)
    node : network node(str)

    """

    # init
    if const.INIT not in context:
        init_rig_hierarchy(context, network)

    # blocks list, context
    blocks = list()
    blocks.append(network)
    blocks_list(network, blocks)
    blocks = [x for x in blocks if not x.hasAttr(const.ISLEGO)]
    for block in blocks:
        common_name, joint_name, side_name, con_exp, jnt_exp = context[const.NAMING]
        block_name = block.attr(const.BLOCK_NAME).get()
        block_side = side_name[block.attr(const.BLOCK_SIDE).get()]
        block_index = block.attr(const.BLOCK_INDEX).get()
        common_name = common_name.format(name=block_name,
                                         side=block_side,
                                         index=block_index,
                                         description="{description}",
                                         extension="{extension}")

        joint_name = joint_name.format(name=block_name,
                                       side=block_side,
                                       index=block_index,
                                       description="{description}",
                                       extension="{extension}")

        name = lib.get_context_name(block, side_name)
        if name not in context:
            log.log(level=0, msg="context {0}".format(name))
            context[name] = OrderedDict()
            context[name][const.NAMING] = (common_name, joint_name, con_exp, jnt_exp)
        else:
            raise Exception("already context {0}".format(name))

    # import blocks
    modules = list()
    for index, block in enumerate(blocks):
        common_name, joint_name, side_name, con_exp, jnt_exp = context[const.NAMING]
        block_type = block.attr(const.BLOCK_TYPE).get()

        name = lib.get_context_name(block, side_name)
        log.log(level=0, msg="init {0}".format(name))
        modules.append(importlib.import_module("lego.blocks.legobox.{0}".format(block_type)))
        # importlib.reload(modules[index])

    # create objects
    for index, module in enumerate(modules):
        side_name = context[const.NAMING][2]
        name = lib.get_context_name(blocks[index], side_name)
        log.log(level=0, msg="Objects {0}".format(name))
        module.create_objects(context, name, blocks[index])

    # create attributes
    for index, module in enumerate(modules):
        side_name = context[const.NAMING][2]
        name = lib.get_context_name(blocks[index], side_name)
        log.log(level=0, msg="Attribute {0}".format(name))
        module.create_attributes(context, name, blocks[index])

    # create connections
    for index, module in enumerate(modules):
        side_name = context[const.NAMING][2]
        name = lib.get_context_name(blocks[index], side_name)
        log.log(level=0, msg="Connections {0}".format(name))
        module.create_connections(context, name, blocks[index])

    # connect joints
    for index, module in enumerate(modules):
        side_name = context[const.NAMING][2]
        name = lib.get_context_name(blocks[index], side_name)
        log.log(level=0, msg="Joint structure {0}".format(name))
        module.joint_structure(context, name, blocks[index])

def clear(context):
    """ Clear scene 

    step 0. rig clean up
    step 1. post script run
    
    context : context(dict)
    node : network root node(str)

    """

    log.log(level=0, msg="clear !")
    log.log(level=0, msg="controller set")
    log.log(level=0, msg="mesh set")
    log.log(level=0, msg="joint set")

    # node = pm.PyNode(node)
    #
    # for script in info[const.POSTSCRIPTS]:
    #     mod = importlib.import_module(script)
    #     mod.PrePost.run(context)

def init_rig_hierarchy(context, network):
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
    world_root = primitive.addTransform(blocks, "world_root", m=origin_matrix)
    world_npo = primitive.addTransform(world_root, "world_npo", m=origin_matrix)
    world_con = icon.create(world_npo, "world_{0}".format(context[const.NAMING][3]), origin_matrix, 17, "compas")
    world_ref = primitive.addTransform(world_con, "world_ref", m=origin_matrix)
    world_output = primitive.addTransform(world_root, "world_output", m=origin_matrix)
    decompose = node.createDecomposeMatrixNode(world_ref.worldMatrix)

    # attribute
    attribute.addAttribute(rig, "controllersVis", "bool", True)
    attribute.addAttribute(rig, "ControllersOnPlaybackVis", "bool", False)
    attribute.addAttribute(rig, "jointsVis", "bool", False)

    # connections
    decompose.outputTranslate >> world_output.t
    decompose.outputRotate >> world_output.r
    decompose.outputScale >> world_output.s
    decompose.outputShear >> world_output.shear

    rig.controllersVis >> blocks.v
    rig.jointsVis >> joints.v
    rig.ControllersOnPlaybackVis >> blocks.hideOnPlayback
    attribute.lockAttribute(rig)
    attribute.lockAttribute(model)
    attribute.lockAttribute(blocks)
    attribute.lockAttribute(joints)
    attribute.lockAttribute(world_root)
    attribute.lockAttribute(world_ref)
    attribute.setKeyableAttributes(world_con)

    guide = network.attr(const.GUIDE).get()
    root_guide = guide.getParent(generations=-1)
    root_network = root_guide.message.outputs(type="network")[0]
    rig.message >> root_network.rig

    log.log(level=0, msg="context {0}".format(const.INIT))
    context[const.INIT] = OrderedDict()
    context[const.INIT]["rig"] = rig
    context[const.INIT]["model"] = model
    context[const.INIT]["blocks"] = blocks
    context[const.INIT]["joints"] = joints
    context[const.INIT]["object"] = [world_root, world_npo, world_con, world_ref, world_output]
    context[const.INIT][const.OUTPUT] = [world_output]
    context[const.INIT][const.BLOCK_UI] = world_con
