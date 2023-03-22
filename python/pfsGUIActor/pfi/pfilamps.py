__author__ = 'alefur'

from pfsGUIActor.control import ControlPanel, CommandsGB, ControlDialog
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.widgets import ValueMRow, ValueGB, SwitchGB, CmdButton, ValuesRow, SwitchMRow


class PfiLampsRow(ModuleRow):
    lampNames = ['Neon', 'Argon', 'Krypton', 'Xenon', 'HgCd', 'QTH']

    def __init__(self, pfiModule, name='pfilamps'):
        ModuleRow.__init__(self, module=pfiModule, actorName=name, actorLabel=name.upper())

        self.lamps = [SwitchMRow(self, f'lampRequestMask', lamp, i, '{:g}') for i, lamp in enumerate(PfiLampsRow.lampNames)]
        self.lampStatus = ValueMRow(self, 'lampStatus', 'lampStatus', 0, '{:s}')
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
        self.lamps = [LampState(self.moduleRow, i, lamp) for i, lamp in enumerate(self.moduleRow.lampNames)]

    def setInLayout(self):
        for i, lamp in enumerate(self.lamps):
            self.grid.addWidget(lamp, i // 3, i % 3)


class LampState(ValuesRow):
    def __init__(self, moduleRow, ind, lamp):
        widgets = [SwitchGB(moduleRow, f'lampRequestMask', '', ind, '{:g}'),
                   ValueGB(moduleRow, f'lampRequestTimes', 'Seconds', ind, '{:d}')]

        ValuesRow.__init__(self, widgets, title=lamp)
        self.grid.setContentsMargins(2, 8, 2, 2)


class PfiLampsCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)

        self.allStatus = CmdButton(controlPanel=controlPanel, label='ALL STATUS', cmdStr='pfilamps allstat')
        self.grid.addWidget(self.allStatus, 1, 0)
