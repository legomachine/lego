# -*- coding:utf-8 -*-

# maya
import pymel.core as pm
import maya.cmds as mc

# core
from lego.core import log


def ready():
    """ Assembly ready

    pre scripts run
    get blocks

    """

def stacking_blocks():
    """ Assemble blocks

    assemble block

    """

def clear():
    """ Clear scene 

    remove guide 
    post scripts run

    """

def get_guide_info():
    """

    get block info 

    """

    try:
        guide = pm.ls("guide", type="transform")[0]
        guide_info = pm.ls("guide_info", type="network")[0]
    except Exception as e:
        log.log(level=2, msg=e)


def custom_scripts(path):
    """

    custom scripts run

    """


