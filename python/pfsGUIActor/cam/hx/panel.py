__author__ = 'alefur'

import pfsGUIActor.styles as styles
from pfsGUIActor.cam import CamDevice
from pfsGUIActor.control import ControllerCmd, ControlPanel
from pfsGUIActor.widgets import ValueGB, ValuesRow


class RampConfig(ValuesRow):
    labels = ['nRamp', 'nGroup', 'nReset', 'nRead', 'nDrop']

    def __init__(self, moduleRow, fontSize=styles.smallFont):
        widgets = [ValueGB(moduleRow, 'ramp', lab, i, '{:d}') for i, lab in enumerate(RampConfig.labels)]
        ValuesRow.__init__(self, widgets, title='rampConfig', fontSize=fontSize)
        self.grid.setContentsMargins(1, 8, 1, 1)


class HxRead(ValuesRow):
    labels = ['visit', 'nRamp', 'nGroup', 'nRead']

    def __init__(self, moduleRow, fontSize=styles.smallFont):
        widgets = [ValueGB(moduleRow, 'hxread', lab, i, '{:d}') for i, lab in enumerate(HxRead.labels)]
        ValuesRow.__init__(self, widgets, title='HxRead', fontSize=fontSize)


class HxPanel(CamDevice):

    def __init__(self, controlDialog):
        # There is hxhal controller but the logic is quite different from the other controllers.
        CamDevice.__init__(self, controlDialog, controllerName='')
        self.addCommandSet(HxCommands(self))

    def createWidgets(self):
        self.rampConfig = RampConfig(self.moduleRow)
        self.hxRead = HxRead(self.moduleRow)
        self.filename = ValueGB(self.moduleRow, 'filename', 'filepath', 0, '{:s}')

    def setInLayout(self):
        self.grid.addWidget(self.rampConfig, 0, 0, 1, 5)
        self.grid.addWidget(self.hxRead, 1, 0, 1, 4)
        self.grid.addWidget(self.filename, 2, 0, 1, 3)

    def setEnabled(self, a0):
        connected = self.moduleRow.isOnline
        return ControlPanel.setEnabled(self, connected)


class HxCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)

    def setEnabled(self, a0: bool):
        """Just disable connect / disconnect."""
        super().setEnabled(a0)
        self.connectButton.setEnabled(False)
        self.connectButton.setVisible(False)
        self.disconnectButton.setEnabled(False)
        self.disconnectButton.setVisible(True)
