# -*- coding:utf-8 -*-

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
__const.KIND = "kind"
__const.WORLD = "world"

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
__const.INPUT = "input"
__const.OUTPUT = "output"
__const.PRESCRIPTS = "preScripts"
__const.POSTSCRIPTS = "postScripts"

__const.MESHES = "meshes"
__const.JOINTS = "joints"
__const.CONTROLLERS = "controllers"

__const.SEPARATOR = ", "

sys.modules[__name__] = __const


