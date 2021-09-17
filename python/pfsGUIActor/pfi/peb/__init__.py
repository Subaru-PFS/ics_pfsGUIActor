__author__ = 'alefur'

import pfsGUIActor.styles as styles
from PyQt5.QtWidgets import QGridLayout
from pfsGUIActor.common import ComboBox
from pfsGUIActor.control import ControlPanel, CommandsGB, ControlDialog
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.pfi.peb.flow import FlowPanel
from pfsGUIActor.pfi.peb.temps import TempsPanel
from pfsGUIActor.pfi.peb.power import PowerPanel
from pfsGUIActor.pfi.peb.led import LedPanel
from pfsGUIActor.widgets import Coordinates, SwitchGB, DoubleSpinBoxGB, CustomedCmd, CmdButton, ValueMRow, Controllers, ValueGB


class PebRow(ModuleRow):
    def __init__(self, module):
        ModuleRow.__init__(self, module=module, actorName='peb', actorLabel='PEB')

        self.controllers = Controllers(self)
        self.createDialog(PebDialog(self))

    @property
    def widgets(self):
        return []


class PebDialog(ControlDialog):
    def __init__(self, pebRow):
        ControlDialog.__init__(self, moduleRow=pebRow)
        self.flowPanel = FlowPanel(self)
        self.tempsPanel = TempsPanel(self)
        self.powerPanel = PowerPanel(self)
        self.ledPanel = LedPanel(self)

        self.tabWidget.addTab(self.flowPanel, 'flow')
        self.tabWidget.addTab(self.tempsPanel, 'temps')
        self.tabWidget.addTab(self.powerPanel, 'power')
        self.tabWidget.addTab(self.ledPanel, 'led')
