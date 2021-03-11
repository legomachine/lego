# -*- coding:utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

from functools import partial

from mgear.core import pyqt, string
from mgear.vendor.Qt import QtCore, QtWidgets, QtGui

# pyside
from maya.app.general.mayaMixin import MayaQDockWidget
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import pymel.core as pm 

# lego
from lego.blocks.legobox import blockcomponentui as bcui
from lego.blocks.legobox import blockrootui as brui
from lego.core.api import const


class BlockComponentUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(BlockComponentUI, self).__init__(parnet=parent)
        self.bcui = bcui.Ui_Form()
        self.bcui.setupUi()     

        self.create_widgets()
        self.create_connections()

        self.root = pm.selected(type="transform")[0]
        self.network = self.root.message.outputs(type="network")[0]

    def create_widgets(self):
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.insertTab(0, self.bcui, "Block Common Setting")
    
    def create_connections(self):
        self.bcui.parent_le.editingFinished.connect(self.update_common)
        self.bcui.ref_cbbox.currentIndexChanged.connect(self.update_common)
        self.bcui.name_le.editingFinished.connect(self.update_common)
        self.bcui.side_le.editingFinished.connect(self.update_common)
        self.bcui.index_spbox.valueChanged.connect(self.update_common)
        self.bcui.joint_cbox.stateChanged.connect(self.update_common)
        self.bcui.ui_btn.clicked.connect(self.update_common)
    
    def update_common(self):
        txt = string.removeInvalidCharacter(self.bcui.parent_le.text())
        parent = pm.PyNode(txt)
        if self.network.attr(const.BLOCK_PARENT).inputs(type="network"):
            pm.disconnectAttr(self.network.attr(const.BLOCK_PARENT))
        parent.attr(const.BLOCK_CHILDREN) >> self.network.attr(const.BLOCK_PARENT)
        outputs = parent.attr(const.OUTPUT)
        output = [outputs[index] for index in outputs.numElements() if outputs[index].get() == self.bcui.ref_cbbox.currentText()]
        if self.network.attr(const.OUTPUT).outputs(type="network"):
            pm.disconnectAttr(self.network.attr(const.OUTPUT))
        if not output:
            output[0] >> self.network.attr(const.BLOCK_PARENT_SPACE)
        txt = string.removeInvalidCharacter(self.bcui.name_le.text())
        self.network.attr(const.BLOCK_NAME).set(txt)
        txt = string.removeInvalidCharacter(self.bcui.side_le.text())
        self.network.attr(const.BLOCK_SIDE).set(txt)
        txt = string.removeInvalidCharacter(self.bcui.index_spbox.value())
        self.network.attr(const.BLOCK_INDEX).set(txt)

    def ui_btn_clicked(self):
        sel = pm.selected(type="transform")
        if not sel:
            return
        network = sel[0].message.outputs(type="network")
        if not network:
            return
        if self.network.attr(const.BLOCK_UI).inputs():
            pm.disconnectAttr(self.network.attr(const.BLOCK_UI))
        network[0].message >> self.network.attr(const.BLOCK_UI)
        self.bcui.ui_le.setText(sel[0].name())
        

class BlockRootUI(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=None):
        pyqt.deleteInstances(self, MayaQDockWidget)

        super(BlockRootUI, self).__init__(parent=parent)
        self.create_widgets()
        self.create_connections()

        self.root = pm.selected(type="transform")[0]
        self.network = self.root.message.outputs(type="network")[0]

    def create_widgets(self):
        pass

    def create_connections(self):
        pass