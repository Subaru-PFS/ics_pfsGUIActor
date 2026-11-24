__author__ = 'alefur'

from functools import partial

import pfsGUIActor.styles as styles
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMenu, QProgressBar
from pfsGUIActor.cam.hx.panel import HxPanel, IRP
from pfsGUIActor.control import ControlDialog, Topbar
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.widgets import Controllers, StaticValueGB


class RampState(StaticValueGB):
    defaultColors = dict(background='green', police='white')
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        self.controllerName = ''
        self.isRamping = False
        self.rampColor = 'skyblue'
        StaticValueGB.__init__(self, moduleRow, '', 'IDLE', fontSize=styles.bigFont)

        self.rampProgress = RampProgress(self)
        self.grid.addWidget(self.rampProgress, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

    def setEnabled(self, isOnline):
        """Keep the ramp colour while a ramp is shown, rather than the idle default."""
        if isOnline and self.isRamping:
            self.setColor(self.rampColor)
        else:
            StaticValueGB.setEnabled(self, isOnline)

    def contextMenuEvent(self, event):
        """Offer to acknowledge a ramp left on display, e.g. one that failed, back to IDLE."""
        if not self.isRamping:
            return

        menu = QMenu(self)
        acknowledgeAction = menu.addAction("Acknowledge")
        if menu.exec_(self.mapToGlobal(event.pos())) == acknowledgeAction:
            self.rampProgress.doShow(False)


class RampProgress(QProgressBar):
    # seconds without a read before a ramp is shown as stuck; twice that for the first, after the resets.
    stuckTimeout = 30

    def __init__(self, rampState):
        QProgressBar.__init__(self)
        self.nreset = 1
        self.nread = 1
        self.rampState = rampState
        self.watchdog = QTimer(self)
        self.watchdog.setSingleShot(True)
        self.watchdog.timeout.connect(partial(self.setRampColor, 'red'))
        self.hxRow = rampState.moduleRow
        self.hxRow.keyVarDict['ramp'].addCallback(self.setRampConfig, callNow=False)
        self.hxRow.keyVarDict['hxread'].addCallback(self.updateBar, callNow=False)
        self.hxRow.keyVarDict['filename'].addCallback(self.setRampConfig, callNow=False)

        self.setStyleSheet("QProgressBar {background-color: rgba(0, 0, 0, 0);color:white;text-align: center; }")

    def setRampConfig(self, keyvar):
        try:
            nramp, ngroup, nreset, nread, ndrop = keyvar.getValue()
        except ValueError:
            self.doShow(False)
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

        self.setValue(int(read))

        if self.rampState.isRamping:
            self.setRampColor('skyblue')
            self.watchdog.start(self.stuckTimeout * 1000)

        if group == 0 and read == self.nreset:
            self.setRange(0, self.nread)
            self.setValue(0)
            self.setFormat('RAMP READ\r\n' + '%v / %m')

        if group == 1 and read == self.nread:
            self.doShow(False)

    def doShow(self, show):
        self.rampState.isRamping = show
        if show:
            self.show()
            self.setRampColor('skyblue')
            self.watchdog.start(2 * self.stuckTimeout * 1000)
            self.rampState.value.hide()
        else:
            self.watchdog.stop()
            self.hide()
            self.rampState.setEnabled(self.hxRow.isOnline)
            self.rampState.value.show()

    def setRampColor(self, color):
        """Colour the box for the ramp on display, and keep that colour for setEnabled."""
        self.rampState.rampColor = color
        self.rampState.setEnabled(self.hxRow.isOnline)


class HxRow(ModuleRow):
    def __init__(self, camRow):
        self.camRow = camRow
        ModuleRow.__init__(self, module=camRow.module,
                           actorName='hx_%s%i' % (camRow.arm, camRow.module.specNum), actorLabel='HX')

        self.controllers = Controllers(self)
        self.substate = RampState(self)
        self.irp = IRP(self, fontSize=styles.bigFont)
        self.actorStatus.button.setEnabled(False)

    @property
    def widgets(self):
        return [self.substate, self.irp]

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
    def panels(self):
        return [self.hxPanel]
