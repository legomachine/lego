# -*- coding:utf-8 -*-
""" guide modules """

# maya
import pymel.core as pm
import pymel.core.datatypes as dt

# mgear
from mgear.core import (
    node, 
    fcurve, 
    applyop, 
    vector, 
    icon,
    attribute,
    transform,
    primitive
)

# lego
from lego.core.api import const

import importlib
import datetime


def is_guide():
    selected = pm.selected(type="transform")
    if selected:
        if selected[0].hasAttr(const.ISLEGOGUIDE):
            root = False
            temp = selected[0]
            while not root:
                root = temp.hasAttr(const.ISROOT)
                if not root:
                    temp = temp.getParent()
                    if not temp:
                        break
            network = temp.message.outputs(type="network")[0]
            return selected[0], network
    return None, None

def init_guide_hierarchy():
    origin = dt.Vector(0, 0, 0)
    origin_matrix = transform.getTransformFromPos(origin)
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")

    # node
    guide = primitive.addTransform(None, "guide", m=origin_matrix)
    controllers = primitive.addTransform(guide, "controllers", m=origin_matrix)
    network = pm.createNode("network")

    # attribute
    attribute.lockAttribute(guide)
    attribute.addAttribute(guide, const.ISLEGOGUIDE, "bool", True, keyable=False)
    attribute.addAttribute(guide, const.ISROOT, "bool", True, keyable=False)
    attribute.addAttribute(controllers, const.ISLEGOGUIDE, "bool", True, keyable=False)

    attribute.addAttribute(network, "name", "string", "rig")
    attribute.addAttribute(network, const.ISLEGO, "bool", True, keyable=False)
    attribute.addAttribute(network, const.CHILDREN, "message")
    attribute.addAttribute(network, const.GUIDE, "message")
    attribute.addAttribute(network, const.RIG, "message")
    network.addAttr(const.PRESCRIPTS, type="string", multi=True)
    network.addAttr(const.POSTSCRIPTS, type="string", multi=True)
    attribute.addAttribute(network, "notes", "string", time)

    # connections
    guide.message >> network.attr(const.GUIDE)

    return guide, network

def add_network(root):
    network = pm.createNode("network")
    attribute.addAttribute(network, const.NAMERULE, "string", "{name}_{side}{index}_{description}_{extension}")
    attribute.addAttribute(network, const.JOINTNAMERULE, "string", "{name}_{side}{index}_{description}_{extension}")
    attribute.addAttribute(network, const.BLOCK_TYPE, "string")
    attribute.addAttribute(network, const.BLOCK_VERSION, "string")
    attribute.addAttribute(network, const.BLOCK_NAME, "string")
    attribute.addAttribute(network, const.BLOCK_SIDE, "string")
    attribute.addAttribute(network, const.BLOCK_INDEX, "string")
    attribute.addAttribute(network, const.BLOCK_UI, "message")
    attribute.addAttribute(network, const.BLOCK_FEATURE, "message")
    attribute.addAttribute(network, const.BLOCK_PARENT, "message")
    attribute.addAttribute(network, const.BLOCK_PARENT_SPACE, "message")
    attribute.addAttribute(network, const.CHILDREN, "message")
    attribute.addAttribute(network, const.GUIDE, "message")
    attribute.addAttribute(network, const.RIG, "message")
    attribute.addAttribute(network, const.JOINT, "bool", True)
    network.addAttr(const.OUTPUT, type="string", multi=True)
    network.addAttr(const.PRESCRIPTS, type="string", multi=True)
    network.addAttr(const.POSTSCRIPTS, type="string", multi=True)
    root.message >> network.attr(const.GUIDE)
    return network

def find_index(name, side):
    selected = pm.selected(type="transform")
    if not selected:
        return str(0)
    top = selected[0].getParent(generations=-1)
    dag_list = pm.ls(top, dag=True, type="transform")
    roots = [x for x in dag_list if x.hasAttr(const.ISROOT)]
    networks = [x.message.outputs(type="network")[0] for x in roots if not x.message.outputs(type="network")[0].hasAttr(const.ISLEGO)]

    names = [x for x in networks if x.attr(const.BLOCK_NAME).get() == name]
    sides = [x for x in names if x.attr(const.BLOCK_SIDE).get() == side]
    index = [int(x.attr(const.BLOCK_INDEX).get()) for x in sides]
    num = 0
    if not index:
        return str(0)
    else:
        while True:
            if num not in index:
                break
            num += 1
        return str(num)
        