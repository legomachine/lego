# -*- coding:utf-8 -*-

# maya
import pymel.core as pm
import maya.cmds as mc


def world(context):
    """ create rig hierarchy 
    rig (hierarchy)
        model
        ---modeling...
        controllers_saver
        ---controller shape...
        blocks
        ---world_grp
        ------world_con
        ---------world_ref
        ---another blocks...
        joints
        ---binding joints...

    context["world"]["rig"] = root
    context["world"]["model"] = model
    context["world"]["blocks"] = blocks
    context["world"]["output"] = world_ref

    """
    rig = pm.group(name="rig", empty=True)
    model = pm.group(name="model", empty=True)
    controllers_saver = pm.group(name="controllers_saver", empty=True)
    blocks = pm.group(name="blocks", empty=True)
    joints = pm.group(name="joints", empty=True)
    world_con = pm.circle(name="world_con", constructionHistory=False)[0]
    world_ref = pm.group(name="world_ref", empty=True)

    rig.addAttr("controllersVis", type="boolean")
    rig.addAttr("jointsVis", type="boolean")
    rig.addAttr("ControllersOnPlaybackVis", type="boolean")
    
    rig.controllersVis >> blocks.v
    rig.jointsVis >> joints.v
    rig.ControllersOnPlaybackVis >> blocks.hideOnPlayback

    pm.parent(model, controllers_saver, blocks, joints, rig)
    pm.parent(world_con, blocks)
    pm.parent(world_ref, world_con)
    
    context["world"] = dict()
    context["world"]["rig"] = rig
    context["world"]["model"] = model
    context["world"]["blocks"] = blocks
    context["world"]["output"] = world_ref

def stacking_block(context, node):
    pass
