__author__ = 'alefur'

from PyQt5.QtWidgets import QProgressBar
from pfsGUIActor.control import ControllerCmd, ControlDialog
from pfsGUIActor.widgets import SubSystemLabel


class EnuDeviceCmd(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel=controlPanel)
        self.addButtons(controlPanel)

    def addButtons(self, controlPanel):
        actor, controller = controlPanel.actorName, controlPanel.controllerName
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s %s status' % (actor, controller))
        self.connectButton = CmdButton(controlPanel=controlPanel, label='START',
                                       cmdStr='%s %s start' % (actor, controller))
        self.disconnectButton = CmdButton(controlPanel=controlPanel, label='STOP',
                                          cmdStr='%s %s STOP' % (actor, controller))
        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)
        self.grid.addWidget(self.disconnectButton, 0, 1)


from pfsGUIActor.enu.bia import BiaPanel
from pfsGUIActor.enu.iis import IisPanel
from pfsGUIActor.enu.pdu import PduPanel
from pfsGUIActor.enu.rexm import RexmPanel
from pfsGUIActor.enu.shutters import ShuttersPanel
from pfsGUIActor.enu.slit import SlitPanel
from pfsGUIActor.enu.temps import TempsPanel
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.widgets import CmdButton, ValueMRow, Controllers, CustomedCmd, SwitchMRow
from pfsGUIActor.common import ComboBox, GridLayout
import pfsGUIActor.styles as styles


class IisCombined(SwitchMRow):
    lamps = ['halogen', 'neon', 'argon', 'krypton']

    def __init__(self, moduleRow):
        class SingleIisLamp(SwitchMRow):
            def __init__(self, iisCombined, lampName):
                self.iisCombined = iisCombined
                SwitchMRow.__init__(self, iisCombined.moduleRow, lampName, lampName, 0, '{:g}', controllerName='iis')

            def setText(self, txt):
                SwitchMRow.setText(self, txt)
                self.iisCombined.setText(txt)

        SwitchMRow.__init__(self, moduleRow, 'argon', 'IIS', 0, '{:g}')

        self.lamps = [SingleIisLamp(self, lamp) for lamp in IisCombined.lamps]

    def setText(self, txt):
        states = [lamp.value.text() for lamp in self.lamps]
        state = 'ON' if any([state == 'ON' for state in states]) else 'OFF'

        self.value.setText(state)
        self.customize()


class ElapsedTime(QProgressBar):
    def __init__(self, enuRow):
        QProgressBar.__init__(self)
        self.enuRow = enuRow
        self.enuRow.keyVarDict['elapsedTime'].addCallback(self.updateBar, callNow=False)
        self.enuRow.keyVarDict['integratingTime'].addCallback(self.setExptime, callNow=False)
        self.setStyleSheet("QProgressBar {font-size: %ipt; background-color: rgba(0, 0, 0, 0);"
                           "color:white;text-align: center; }" % styles.bigFont)
        self.setFormat('EXPOSING \r\n' + '%v / %m secs')

    def setExptime(self, keyvar):
        try:
            exptime = int(round(keyvar.getValue()))
        except ValueError:
            return

        self.setRange(0, exptime)

    def updateBar(self, keyvar):
        try:
            val = int(round(keyvar.getValue()))
        except ValueError:
            val = 0

        self.setValue(val)

    def resetValue(self):
        self.hide()
        self.setValue(0)


class Substate(ValueMRow):
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        ValueMRow.__init__(self, moduleRow, 'metaFSM', '', 1, '{:s}')
        self.elapsedTime = ElapsedTime(moduleRow)
        self.grid.addWidget(self.elapsedTime, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

    def setText(self, txt):

        txt = txt.upper()
        if txt in ['EXPOSING', 'OPENRED', 'OPENBLUE']:
            self.value.hide()
            self.elapsedTime.show()
        else:
            self.value.show()
            self.elapsedTime.resetValue()

        ValueMRow.setText(self, txt)


class EnuRow(ModuleRow):
    def __init__(self, specModule):
        ModuleRow.__init__(self, module=specModule, actorName='enu_sm%i' % specModule.specNum, actorLabel='ENU')

        self.state = ValueMRow(self, 'metaFSM', '', 0, '{:s}')
        self.substate = Substate(self)

        self.rexm = ValueMRow(self, 'rexm', 'Red Resolution', 0, '{:s}', controllerName='rexm')
        self.slit = ValueMRow(self, 'slitPosition', 'Slit', 0, '{:s}', controllerName='slit')
        self.shutters = ValueMRow(self, 'shutters', 'Shutters', 0, '{:s}', controllerName='biasha')
        self.bia = ValueMRow(self, 'bia', 'BIA', 0, '{:s}', controllerName='biasha')
        self.iis = IisCombined(self)

        self.controllers = Controllers(self)

        self.createDialog(EnuDialog(self))

    @property
    def widgets(self):
        return [self.state, self.substate, self.rexm, self.slit, self.shutters, self.bia, self.iis]


class ConnectButton(CmdButton):
    def __init__(self, upperCmd, label):
        self.upperCmd = upperCmd
        CmdButton.__init__(self, controlPanel=None, controlDialog=upperCmd.controlDialog, label=label)

    def buildCmd(self):
        return self.upperCmd.buildCmd()


class ConnectCmd(CustomedCmd):
    def __init__(self, controlDialog, controllers):
        GridLayout.__init__(self)
        self.keyvar = controlDialog.moduleRow.keyVarDict['controllers']
        self.keyvar.addCallback(self.setButtonLabel, callNow=False)
        self.controlDialog = controlDialog
        self.button = ConnectButton(self, label='CONNECT')

        self.combo = ComboBox()
        self.combo.addItems(controllers)
        self.combo.currentTextChanged.connect(self.setButtonLabel)

        self.addWidget(self.button, 0, 0)
        self.addWidget(self.combo, 0, 1)

    def setButtonLabel(self, keyvar):
        keyvar = self.keyvar if isinstance(keyvar, str) else keyvar
        controllers = keyvar.getValue(doRaise=False)
        label = 'DISCONNECT' if self.combo.currentText() in controllers else 'CONNECT'
        self.button.setText(label)

    def buildCmd(self):
        cmdStr = '%s %s controller=%s ' % (self.controlDialog.moduleRow.actorName, self.button.text().lower(),
                                           self.combo.currentText())
        return cmdStr


class EnuDialog(ControlDialog):
    def __init__(self, enuRow):
        ControlDialog.__init__(self, moduleRow=enuRow, title='Entrance Unit SM%i' % enuRow.module.specNum,
                               addGridRows=12)

        self.startButton = CmdButton(controlPanel=None, label=' START ', controlDialog=self,
                                     cmdStr='%s start' % self.moduleRow.actorName)

        self.stopButton = CmdButton(controlPanel=None, label=' STOP ', controlDialog=self,
                                    cmdStr='%s stop' % self.moduleRow.actorName)
        self.connectCmd = ConnectCmd(self, ['rexm', 'biasha', 'slit', 'temps', 'pdu', 'iis'])

        self.topbar.addWidget(self.startButton)
        self.topbar.addWidget(self.stopButton)

        self.topbar.addLayout(self.connectCmd)

        self.slitPanel = SlitPanel(self)
        self.shuttersPanel = ShuttersPanel(self)
        self.biaPanel = BiaPanel(self)
        self.rexmPanel = RexmPanel(self)
        self.tempsPanel = TempsPanel(self)
        self.pduPanel = PduPanel(self)
        self.iisPanel = IisPanel(self)

        self.tabWidget.addTab(self.slitPanel, 'FCA')
        self.tabWidget.addTab(self.shuttersPanel, 'SHUTTERS')
        self.tabWidget.addTab(self.biaPanel, 'BIA')
        self.tabWidget.addTab(self.rexmPanel, 'RDA')
        self.tabWidget.addTab(self.tempsPanel, 'TEMPS')
        self.tabWidget.addTab(self.pduPanel, 'PDU')
        self.tabWidget.addTab(self.iisPanel, 'IIS')

        self.grid.addWidget(SubSystemLabel(f'SM{enuRow.module.specNum}', color='black', fontsize=20), 0, 8, 2, 1)
