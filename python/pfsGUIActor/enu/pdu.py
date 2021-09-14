__author__ = 'alefur'

from pfsGUIActor.control import ControllerPanel, ControllerCmd
from pfsGUIActor.widgets import ValueGB, SwitchGB, ValuesRow, SwitchButton
from pfsGUIActor.enu import EnuDeviceCmd


class PduButton(SwitchButton):
    def __init__(self, controlPanel, pduPort):
        cmdStrOn = '%s power on=%s' % (controlPanel.actorName, pduPort.powerName)
        cmdStrOff = '%s power off=%s' % (controlPanel.actorName, pduPort.powerName)
        SwitchButton.__init__(self, controlPanel=controlPanel, key=pduPort.pduPort,
                              label=pduPort.powerName.capitalize(), ind=1, fmt='{:s}', cmdHead='', cmdStrOn=cmdStrOn,
                              cmdStrOff=cmdStrOff)

    def setText(self, txt):
        txt = 1 if txt == 'on' else 0
        return SwitchButton.setText(self, txt=txt)


class PduPort(ValuesRow):
    def __init__(self, moduleRow, powerName, pduPort):
        self.powerName = powerName
        self.pduPort = pduPort
        widgets = [SwitchGB(moduleRow, pduPort, 'state', 1, '{:s}'),
                   ValueGB(moduleRow, pduPort, 'volts', 2, '{:.3f}'),
                   ValueGB(moduleRow, pduPort, 'amps', 3, '{:.3f}'),
                   ValueGB(moduleRow, pduPort, 'watts', 4, '{:.3f}')]

        ValuesRow.__init__(self, widgets, title=f'{powerName.capitalize()}')


class PduPanel(ControllerPanel):
    ports = dict(slit=3, ctrl=4, pows=5, hgar=6, neon=7, temps=8)

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'pdu')
        self.grid.setSpacing(0)
        self.addCommandSet(PduCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'pduMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'pduFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'pduFSM', '', 1, '{:s}')

        self.pduPorts = [PduPort(self.moduleRow, name, f'pduPort{portNb}') for name, portNb in self.ports.items()]

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        for i, pduPort in enumerate(self.pduPorts):
            self.grid.addWidget(pduPort, 1 + i, 0, 1, 4)


class PduCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)
        for i, pduPort in enumerate(controlPanel.pduPorts):
            self.grid.addWidget(PduButton(controlPanel, pduPort), 1 + i, 0)
