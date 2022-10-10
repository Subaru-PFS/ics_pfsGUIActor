__author__ = 'alefur'

import pfs.instdata.io as configIO
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from pfsGUIActor.common import ComboBox, GridLayout
from pfsGUIActor.control import ControlDialog, ControllerPanel
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.widgets import StaticValueGB, ValueGB, CmdButton, ValueMRow, Controllers, \
    CustomedCmd


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

        controller = self.combo.currentText()

        # Should have normalized rough actor names to rough_N.
        if '_' in controller:
            name = controller
            model = name.split('_')[0]
        elif controller[-1].isdigit() and controller != 'gen2':
            name = controller
            model = controller[:-1]
        else:
            name = model = controller

        doConnect = self.button.text().lower() == 'connect'

        if doConnect:
            cmdStr = f'alerts connect controller={model} name={name}'
        else:
            cmdStr = f'alerts disconnect controller={name}'

        return cmdStr


class AlertsRow(ModuleRow):
    def __init__(self, module):
        ModuleRow.__init__(self, module=module, actorName='alerts', actorLabel='')

        self.status = ValueMRow(self, 'alertStatus', 'ALERTS', 0, '{:s}')

        self.status.grid.addWidget(self.actorStatus.button, 0, 0)
        self.controllers = Controllers(self)
        self.createDialog(AlertsDialog(self))

    @property
    def widgets(self):
        return [self.status]


class AlertStatus(ValueGB):
    def __init__(self, controllerPanel, keyName):
        self.controllerPanel = controllerPanel
        self.keyName = keyName
        ValueGB.__init__(self, controllerPanel.moduleRow, keyName, 'status', 2, '{:s}')

    def getStyles(self, text):
        if text == 'OK':
            toolTip = self.getLastTransition('lastAlert')
        else:
            toolTip = self.getLastTransition('lastOK')
            text = 'ALERT'

        self.value.setToolTip(toolTip)
        self.controllerPanel.updateStatusIcon(True)
        self.controllerPanel.adjustSize()
        return ValueGB.getStyles(self, text)

    def getLastTransition(self, transition):
        keyVar = self.moduleRow.keyVarDict[f'{self.keyName}_{transition}']
        try:
            timestamp, value, status = keyVar.getValue()
            toolTip = f'{transition}({timestamp})   value={value}   status={status}'
        except:
            toolTip = f'{transition}=None'

        return toolTip


class AlertLogic(ValueGB):
    def __init__(self, controllerPanel, keyName, *args):
        ValueGB.__init__(self, controllerPanel.moduleRow, f'{keyName}_logic', 'alertLogic', 0, '{:s}')

    def getStyles(self, text):
        text = 'ON' if text != "OFF" else text
        return ValueGB.getStyles(self, text)


class AlertObject:
    def __init__(self, controllerPanel, keyVarName, keyConfig):
        index = f'_{keyConfig["keyName"]}' if keyConfig["keyName"] else ''
        keyName = f'{controllerPanel.controllerName}__{keyVarName}{index}'

        stsId = StaticValueGB(controllerPanel.moduleRow, 'stsId', str(keyConfig["stsId"]))
        stsId.setEnabled(True)

        alertLogic = AlertLogic(controllerPanel, keyName)
        timestamp = ValueGB(controllerPanel.moduleRow, keyName, 'timestamp', 0, '{:s}')
        value = ValueGB(controllerPanel.moduleRow, keyName, keyConfig["stsHelp"], 1, '{:g}')
        status = AlertStatus(controllerPanel, keyName)

        self.stsId = stsId
        self.alertLogic = alertLogic
        self.timestamp = timestamp
        self.value = value
        self.status = status

    @property
    def isInAlert(self):
        return self.status.value.text() != 'OK'


class AlertPanel(ControllerPanel):

    def __init__(self, controlDialog, actorName, stsConfig):
        self.stsConfig = stsConfig
        self.alerts = []
        ControllerPanel.__init__(self, controlDialog, actorName)

    def createWidgets(self):
        for keyVarName, keysConfig in self.stsConfig.items():
            for keyConfig in keysConfig:
                rowId = len(self.alerts)

                alert = AlertObject(self, keyVarName, keyConfig)

                self.grid.addWidget(alert.stsId, rowId, 0)
                self.grid.addWidget(alert.alertLogic, rowId, 1)
                self.grid.addWidget(alert.timestamp, rowId, 2)
                self.grid.addWidget(alert.value, rowId, 3)
                self.grid.addWidget(alert.status, rowId, 4)

                self.alerts.append(alert)

    def setInLayout(self):
        """Set spacer"""
        self.spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.grid.addItem(self.spacer, self.grid.rowCount(), 0)

    def updateStatusIcon(self, a0):
        if not a0:
            return self.updateIcon('gray')

        if any([alert.isInAlert for alert in self.alerts]):
            self.updateIcon('red')
        else:
            self.updateIcon('green')


class AlertsDialog(ControlDialog):
    def __init__(self, alertsRow):
        ControlDialog.__init__(self, moduleRow=alertsRow, title='ALERTS')

        stsConfig, alertsActorConfig = self.loadAlertsConfig()

        # hackity hack.
        actorNames = [f'xcu_{part}' if part not in stsConfig.keys() else part for part in alertsActorConfig['parts']]

        # add connect button
        self.connectCmd = ConnectCmd(self, actorNames)
        self.topbar.addLayout(self.connectCmd)

        for actorName in actorNames:
            alertPannel = AlertPanel(self, actorName, stsConfig[actorName])
            self.tabWidget.addTab(alertPannel, actorName)

    @property
    def site(self):
        return self.moduleRow.module.mwindow.actor.site

    def loadAlertsConfig(self):

        stsConfig = configIO.loadConfig('STS', subDirectory='alerts')['actors']
        alertsActorConfig = configIO.loadConfig('alerts', subDirectory='actors')['alerts'][self.site]

        # extending STS config with optional local configuration.
        if 'extendSTS' in alertsActorConfig:
            moreCfg = configIO.loadConfig(alertsActorConfig['extendSTS'], subDirectory='alerts')
            stsConfig.update(moreCfg['actors'])

        return stsConfig, alertsActorConfig
