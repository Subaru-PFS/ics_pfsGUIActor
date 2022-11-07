__author__ = 'alefur'

from pfsGUIActor.control import ControllerPanel, ControllerCmd
from pfsGUIActor.widgets import ValueGB, SwitchButton, SwitchGB
from pfsGUIActor.enu import EnuDeviceCmd

class ArcButton(SwitchButton):
    def __init__(self, controlPanel, arc):
        cmdStrOn = '%s iis on=%s' % (controlPanel.actorName, arc)
        cmdStrOff = '%s iis off=%s' % (controlPanel.actorName, arc)
        SwitchButton.__init__(self, controlPanel=controlPanel, key=arc, label=arc.capitalize(), cmdHead='',
                              cmdStrOn=cmdStrOn, cmdStrOff=cmdStrOff)


class IisPanel(ControllerPanel):

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'iis')
        self.addCommandSet(IisCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'iisMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'iisFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'iisFSM', '', 1, '{:s}')

        self.argon = SwitchGB(self.moduleRow, 'argon', 'argon', 0, '{:g}')
        self.neon = SwitchGB(self.moduleRow, 'neon', 'Neon', 0, '{:g}')
        self.krypton = SwitchGB(self.moduleRow, 'krypton', 'Krypton', 0, '{:g}')
        self.halogen = SwitchGB(self.moduleRow, 'halogen', 'Halogen', 0, '{:g}')


    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.argon, 1, 0)
        self.grid.addWidget(self.neon, 2, 0)
        self.grid.addWidget(self.krypton, 3, 0)
        self.grid.addWidget(self.halogen, 4, 0)


class IisCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)
        self.grid.addWidget(ArcButton(controlPanel, 'argon'), 1, 0)
        self.grid.addWidget(ArcButton(controlPanel, 'neon'), 2, 0)
        self.grid.addWidget(ArcButton(controlPanel, 'krypton'), 3, 0)
        self.grid.addWidget(ArcButton(controlPanel, 'halogen'), 4, 0)
