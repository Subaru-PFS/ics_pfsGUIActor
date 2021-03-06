__author__ = 'alefur'

import pfsGUIActor.styles as styles
from PyQt5.QtWidgets import QGroupBox, QGridLayout
from pfsGUIActor.control import ControllerPanel, ControllerCmd
from pfsGUIActor.widgets import ValueGB, CmdButton
from pfsGUIActor.enu import EnuDeviceCmd


class Slot(QGroupBox):
    posName = ['X', 'Y', 'Z', 'U', 'V', 'W']

    def __init__(self, moduleRow, nb, fontSize=styles.smallFont):
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        title = 'Slot%d' % nb
        key = 'temps%s' % title
        self.widgets = [ValueGB(moduleRow, key, 'Company', 0, '{:s}', fontSize),
                        ValueGB(moduleRow, key, 'modelNumber', 1, '{:s}', fontSize),
                        ValueGB(moduleRow, key, 'serialNumber', 2, '{:d}', fontSize),
                        ValueGB(moduleRow, key, 'firmware', 3, '{:.1f}', fontSize)]

        for i, widget in enumerate(self.widgets):
            self.grid.addWidget(widget, 0, i)

        self.grid.setContentsMargins(1, 8, 1, 1)
        self.setTitle(title)
        self.setLayout(self.grid)
        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 1ex;} " % (fontSize) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

    def setEnabled(self, a0: bool):
        QGroupBox.setEnabled(self, a0)
        for widget in [self.grid.itemAt(i).widget() for i in range(self.grid.count())]:
            widget.setEnabled(a0)


class TempsPanel(ControllerPanel):
    probeNames1 = ['Motor RDA',
                   'Motor Shutter B',
                   'Motor Shutter R',
                   'BIA Box Top',
                   'BIA Box Bottom',
                   'Fiber Unit Hexapod Bottom',
                   'Fiber Unit Hexapod Top',
                   'Fiber Unit Fiber Frame Top',
                   'Collimator Frame Bottom',
                   'Collimator Frame Top']
    probeNames2 = ['Bench Left Top',
                   'Bench Left Botton',
                   'Bench Right Top',
                   'Bench Right Bottom',
                   'Bench Far Top',
                   'Bench Far Bottom',
                   'Bench Near Top',
                   'Bench Near Bottom',
                   'Bench Central Top',
                   'Enu Temp 20']

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'temps')
        self.addCommandSet(TempsCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'tempsMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'tempsFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'tempsFSM', '', 1, '{:s}')

        self.statusMsg = ValueGB(self.moduleRow, 'tempsStatus', 'Status', 1, '{:s}')

        self.slot1 = Slot(self.moduleRow, 1)
        self.slot2 = Slot(self.moduleRow, 2)

        self.temps1 = [ValueGB(self.moduleRow, 'temps1', name, i, '{:.3f}') for i, name in enumerate(self.probeNames1)]
        self.temps2 = [ValueGB(self.moduleRow, 'temps2', name, i, '{:.3f}') for i, name in enumerate(self.probeNames2)]

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)
        self.grid.addWidget(self.statusMsg, 0, 3)
        #self.grid.addWidget(self.slot1, 1, 0, 1, 4)
        #self.grid.addWidget(self.slot2, 2, 0, 1, 4)
        for i, value in enumerate(self.temps1 + self.temps2):
            self.grid.addWidget(value, 1 + i % 5, i // 5)


class TempsCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
        self.getError = CmdButton(controlPanel=controlPanel, label='ERROR',
                                  cmdStr='%s temps error' % controlPanel.actorName)
        self.getInfo = CmdButton(controlPanel=controlPanel, label='INFO',
                                 cmdStr='%s temps info' % controlPanel.actorName)
        self.getResistance = CmdButton(controlPanel=controlPanel, label='RESISTANCES',
                                       cmdStr='%s temps resistance' % controlPanel.actorName)

        self.grid.addWidget(self.getError, 1, 0)
        self.grid.addWidget(self.getInfo, 1, 1)
        self.grid.addWidget(self.getResistance, 2, 0)
