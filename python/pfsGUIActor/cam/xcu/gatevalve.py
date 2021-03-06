__author__ = 'alefur'
from functools import partial

from pfsGUIActor.cam import CamDevice
from pfsGUIActor.common import CheckBox
from pfsGUIActor.control import ControllerCmd
from pfsGUIActor.widgets import ValueGB, CmdButton, CustomedCmd


class OpenCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='OPEN', safetyCheck=True)

        self.atAtmosphere = CheckBox('atAtmosphere')
        self.underVacuum = CheckBox('underVacuum')
        self.dryRun = CheckBox('dryRun')

        self.atAtmosphere.setChecked(True)
        self.underVacuum.setChecked(False)
        self.dryRun.setChecked(False)

        self.atAtmosphere.stateChanged.connect(partial(self.stateChanged, self.underVacuum))
        self.underVacuum.stateChanged.connect(partial(self.stateChanged, self.atAtmosphere))

        self.addWidget(self.atAtmosphere, 0, 1)
        self.addWidget(self.underVacuum, 0, 2)
        self.addWidget(self.dryRun, 0, 3)

    def stateChanged(self, other, state):
        state = 2 if not state else 0
        other.blockSignals(True)
        other.setChecked(state)
        other.blockSignals(False)

    def buildCmd(self):
        atAtmosphere = 'atAtmosphere' if self.atAtmosphere.isChecked() else ''
        underVacuum = 'underVacuum' if self.underVacuum.isChecked() else ''
        dryRun = 'dryRun' if self.dryRun.isChecked() else ''

        return '%s gatevalve open %s %s %s' % (self.controlPanel.actorName, atAtmosphere, underVacuum, dryRun)


class GVPanel(CamDevice):
    def __init__(self, controlDialog):
        CamDevice.__init__(self, controlDialog, 'gatevalve')
        self.addCommandSet(GVCommands(self))

    def createWidgets(self):
        self.position = ValueGB(self.moduleRow, 'gatevalve', 'Position', 1, '{:s}')
        self.requested = ValueGB(self.moduleRow, 'gatevalve', 'Requested', 2, '{:s}')
        self.samPOW = ValueGB(self.moduleRow, 'sampower', 'SAM POWER', 0, '{:g}')

    def setInLayout(self):
        self.grid.addWidget(self.position, 0, 0)
        self.grid.addWidget(self.requested, 0, 1)
        self.grid.addWidget(self.samPOW, 1, 0)


class GVCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)

        self.openCmd = OpenCmd(controlPanel=controlPanel)
        self.closeButton = CmdButton(controlPanel=controlPanel, label='CLOSE',
                                     cmdStr='%s gatevalve close' % controlPanel.actorName, safetyCheck=True)

        self.openCmd.addWidget(self.closeButton, 1, 0)
        self.grid.addLayout(self.openCmd, 2, 0, 1, 3)
