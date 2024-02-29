__author__ = 'alefur'

from pfsGUIActor.control import ControlPanel, CommandsGB, ControlDialog
from pfsGUIActor.lampUtils import getLampLabel
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.widgets import SwitchGB, CmdButton, SwitchMRow


class PfiLampsRow(ModuleRow):
    lampKeys = ['halogen', 'neon', 'argon', 'krypton', 'xenon', 'hgcd']

    def __init__(self, pfiModule, name='pfilamps'):
        ModuleRow.__init__(self, module=pfiModule, actorName=name, actorLabel=name.upper())

        self.lamps = [SwitchMRow(self, key, getLampLabel(key), 0, '{:g}') for key in self.lampKeys]

        self.createDialog(PfiLampsDialog(self))

    @property
    def widgets(self):
        return self.lamps


class PfiLampsDialog(ControlDialog):
    def __init__(self, pfilampsRow):
        ControlDialog.__init__(self, moduleRow=pfilampsRow)
        self.controlPanel = PfiLampsPanel(self)
        self.tabWidget.addTab(self.controlPanel, '')


class PfiLampsPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)
        self.addCommandSet(PfiLampsCommands(self))

    def createWidgets(self):
        self.lamps = [SwitchGB(self.moduleRow, key, getLampLabel(key), 0, '{:g}') for key in self.controlDialog.moduleRow.lampKeys]

    def setInLayout(self):
        for i, lamp in enumerate(self.lamps):
            self.grid.addWidget(lamp, i, 0)


class PfiLampsCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)

        self.allStatus = CmdButton(controlPanel=controlPanel, label='ALL STATUS', cmdStr='pfilamps allstat')
        self.grid.addWidget(self.allStatus, 1, 0)
