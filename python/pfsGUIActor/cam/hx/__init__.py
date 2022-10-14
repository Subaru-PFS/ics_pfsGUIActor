__author__ = 'alefur'

import pfsGUIActor.styles as styles
from PyQt5.QtWidgets import QProgressBar
from pfsGUIActor.cam.hx.panel import HxPanel
from pfsGUIActor.control import ControlDialog, Topbar
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.widgets import Controllers, StaticValueGB


class RampState(StaticValueGB):
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        self.controllerName = ''
        StaticValueGB.__init__(self, moduleRow, '', 'IDLE', fontSize=styles.bigFont)

        self.rampProgress = RampProgress(self)
        self.grid.addWidget(self.rampProgress, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)


class RampProgress(QProgressBar):
    def __init__(self, rampState):
        QProgressBar.__init__(self)
        self.rampState = rampState
        self.hxRow = rampState.moduleRow
        self.hxRow.keyVarDict['ramp'].addCallback(self.setRampConfig, callNow=False)
        self.hxRow.keyVarDict['hxread'].addCallback(self.updateBar, callNow=False)

        self.setStyleSheet("QProgressBar {background-color: rgba(0, 0, 0, 0);color:white;text-align: center; }")

    def setRampConfig(self, keyvar):
        try:
            nramp, ngroup, nreset, nread, ndrop = keyvar.getValue()
        except ValueError:
            return

        self.doShow(True)

        self.nreset = nreset
        self.nread = nread

        self.setRange(0, nreset)
        self.setValue(0)
        self.setFormat('RESET READ\r\n' + '%v / %m')

    def updateBar(self, keyvar):
        try:
            visit, ramp, group, read = keyvar.getValue()
        except ValueError:
            self.setValue(0)
            return

        self.setValue(read)

        if group == 0 and read == self.nreset:
            self.setRange(0, self.nread)
            self.setValue(0)
            self.setFormat('RAMP READ\r\n' + '%v / %m')

        if group == 1 and read == self.nread:
            self.doShow(False)

    def doShow(self, show):
        if show:
            self.show()
            self.rampState.setColor('skyblue')
            self.rampState.value.hide()
        else:
            self.hide()
            self.rampState.setColor('green')
            self.rampState.value.show()


class HxRow(ModuleRow):
    def __init__(self, camRow):
        self.camRow = camRow
        ModuleRow.__init__(self, module=camRow.module,
                           actorName='hx_%s%i' % (camRow.arm, camRow.module.smId), actorLabel='HX')

        self.controllers = Controllers(self)
        self.substate = RampState(self)
        self.actorStatus.button.setEnabled(False)

    @property
    def widgets(self):
        return [self.substate]

    def setOnline(self):
        ModuleRow.setOnline(self)
        self.camRow.setOnline()

    def createDialog(self, tabWidget):
        self.controlDialog = HxDialog(self, tabWidget)


class HxDialog(ControlDialog):
    def __init__(self, hxRow, tabWidget):
        self.moduleRow = hxRow
        self.tabWidget = tabWidget

        self.topbar = Topbar(self)
        self.topbar.insertWidget(0, self.moduleRow.actorStatus)

        self.hxPanel = HxPanel(self)
        self.tabWidget.addTab(self.hxPanel, 'Hx')

    @property
    def cmdBuffer(self):
        return self.moduleRow.camRow.controlDialog.cmdBuffer

    @property
    def pannels(self):
        return [self.hxPanel]
