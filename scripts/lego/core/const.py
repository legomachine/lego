# -*- coding:utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

# 
import sys

class _const(object):
    class ConstError(TypeError): pass
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const({0})".format(name)) 
        self.__dict__[name] = value


__const = _const()

__const.ISLEGO = "isLego"
__const.ISLEGOGUIDE = "isLegoGuide"
__const.ISLEGORIG = "isLegoRig"
__const.ISROOT = "isRoot"
__const.INIT = "init"

__const.ASSEMBLY = "assembly"
__const.COMPONENT = "component"

__const.BLOCK_TYPE = "blockType"
__const.BLOCK_VERSION = "blockVersion"
__const.BLOCK_NAME = "blockName"
__const.BLOCK_SIDE = "blockSide"
__const.BLOCK_INDEX = "blockIndex"
__const.BLOCK_FEATURE = "blockFeature"
__const.BLOCK_UI = "blockUi"
__const.BLOCK_PARENT = "blockParent"
__const.BLOCK_PARENT_SPACE = "blockParentSpace"

__const.CHILDREN = "children"
__const.GUIDE = "guide"
__const.RIG = "rig"
__const.OUTPUT = "output"
__const.PRESCRIPTS = "preScripts"
__const.POSTSCRIPTS = "postScripts"

__const.MESHES = "meshes"
__const.JOINT = "joint"
__const.CONTROLLERS = "controllers"

__const.SEPARATOR = ", "
__const.STEP = "step"

__const.NAMERULE = "nameRule"
__const.JOINTNAMERULE = "jointNameRule"
sys.modules[__name__] = __const


