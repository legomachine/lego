# -*- coding:utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

# lego
from lego.blocks import (
    lib,
    blueprint,
    assembler,
)

import importlib

# maya
import pymel.core as pm


def draw_blueprint(block):
    mod = importlib.import_module("lego.blocks.legobox.{0}.blueprint".format(block))
    mod.draw()

def build_rig():
    context = dict()
    node = assembler.ready(context)
    assembler.stacking_blocks(context, node)
    assembler.clear(context)

def show_setting():
    pass

__all__ = [
    "lib",
    "blueprint",
    "assembler",
    "draw_blueprint",
    "stacking",
]