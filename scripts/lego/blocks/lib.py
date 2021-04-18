# -*- coding:utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

# lego
from lego.core.api import const, log

# maya
import pymel.core as pm


def get_node_name(rule, description="", extension=""):
    name = rule.format(description=description, extension=extension)
    split_name = [x for x in name.split("_") if x]
    return "_".join(split_name)

def get_context_name(network, side):
    if network.hasAttr(const.ISLEGO):
        return const.INIT
    block_name = network.attr(const.BLOCK_NAME).get()
    block_side = side[network.attr(const.BLOCK_SIDE).get()]
    block_index = network.attr(const.BLOCK_INDEX).get()
    return "{0}_{1}{2}".format(block_name, block_side, block_index)

def get_parent_space(network, context):
    parent_block = network.attr(const.BLOCK_PARENT).get()
    parent_block_space_check = network.attr(const.BLOCK_PARENT_SPACE).inputs(plugs=True)[0].get()
    name = get_context_name(parent_block, context[const.NAMING][2])

    if name not in context:
        outputs = context[const.INIT][const.OUTPUT]
    else:
        outputs = context[name][const.OUTPUT]

    for output in outputs:
        if parent_block_space_check in output.nodeName():
            parent_block_space = output
        else:
            log.log(level=1, msg="parent space nothing")
            parent_block_space = context[const.INIT][const.OUTPUT][0]

    return parent_block_space

def get_parent_joint(network, context):
    parent_block = network.attr(const.BLOCK_PARENT).get()
    parent_block_space_check = network.attr(const.BLOCK_PARENT_SPACE).inputs(plugs=True)[0].get()
    name = get_context_name(parent_block, context[const.NAMING][2])

    if (name not in context) or (name is const.INIT):
        if context[const.INIT][const.OUTPUT][0].message.outputs():
            return context[const.INIT][const.OUTPUT][0].message.outputs()[0]
        else:
            return context[const.INIT]["joints"]

    outputs = context[name][const.OUTPUT]
    joint = None
    for output in outputs:
        if (parent_block_space_check in output.nodeName()) and (output.message.outputs()):
            joint = output.message.outputs()[0]
    if joint:
        return joint
    else:
        return get_parent_joint(parent_block, context)

def connect_joint_space(world, parentInverse, joint):
    mult1 = pm.createNode("multMatrix")
    world >> mult1.matrixIn[0]
    parentInverse >> mult1.matrixIn[1]

    mult2 = pm.createNode("multMatrix")
    mult1.matrixSum >> mult2.matrixIn[0]
    mult2.matrixIn[1].set(mult1.matrixSum.get().inverse())
    mult2.matrixIn[2].set(mult2.matrixSum.get().inverse())

    decom0 = pm.createNode("decomposeMatrix")
    mult1.matrixSum >> decom0.inputMatrix
    decom0.outputTranslate >> joint.t
    decom0.outputScale >> joint.s
    decom0.outputShear >> joint.shear

    decom1 = pm.createNode("decomposeMatrix")
    mult2.matrixSum >> decom1.inputMatrix
    decom1.outputRotate >> joint.r

    joint.jointOrient.set(decom0.outputRotate.get())
    mult2.matrixIn[2].set(joint.inverseMatrix.get())


def get_joint_name():
    pass

class BlockData(object):
    pass
