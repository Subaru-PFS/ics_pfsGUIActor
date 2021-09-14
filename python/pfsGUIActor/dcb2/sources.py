__author__ = 'alefur'

from pfsGUIActor.control import ControllerPanel
from pfsGUIActor.dcb.sources import SwitchLamp
from pfsGUIActor.enu import EnuDeviceCmd
from pfsGUIActor.enu.pdu import PduPort, PduButton
from pfsGUIActor.widgets import ValueGB


class SourcesPanel(ControllerPanel):
    ports = dict(hgar=2, neon=3, xenon=4, krypton=5, argon=6, halogen=8)
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'sources')
        self.addCommandSet(SourcesCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'sourcesMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'sourcesFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'sourcesFSM', '', 1, '{:s}')

        self.pduPorts = [PduPort(self.moduleRow, name, f'pduPort{portNb}') for name, portNb in self.ports.items()]

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        for i, pduPort in enumerate(self.pduPorts):
            self.grid.addWidget(pduPort, 1 + i, 0, 1, 4)


class SourcesCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)
        for i, (nOutlet, source) in enumerate(sorted([(v, k) for k, v in controlPanel.ports.items()], key=lambda l: l[0])):
            self.grid.addWidget(SwitchLamp(controlPanel, source), i+1, 0)

        #self.grid.addWidget(PduButton(controlPanel,  controlPanel.pduPorts[5]), 6, 0)
        #self.grid.addWidget(PduButton(controlPanel, controlPanel.pduPorts[6]), 7, 0)
