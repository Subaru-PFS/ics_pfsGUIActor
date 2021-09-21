__author__ = 'alefur'

import pfsGUIActor.styles as styles
from pfsGUIActor.common import LineEdit
from pfsGUIActor.control import ControlDialog
from pfsGUIActor.control import ControlPanel, CommandsGB, ControlDialog
from pfsGUIActor.enu import ConnectCmd
from pfsGUIActor.modulerow import ModuleRow, RowWidget
from pfsGUIActor.widgets import ValueMRow, SwitchMRow, Controllers, ValueGB, SwitchGB, CmdButton, ValuesRow


class PfiLampsRow(ModuleRow):
    lampNames = [('Argon', 'Ar'), ('Krypton', 'Kr'), ('Neon', 'Ne'), ('Xenon', 'Xe'), ('Hg', 'Hg'), ('Cd', 'Cd'),
                 ('Continuum', 'Cont')]

    def __init__(self, pfiModule, name='pfilamps'):
        ModuleRow.__init__(self, module=pfiModule, actorName=name, actorLabel=name.upper())

        self.lamps = [SwitchGB(self, f'{lamp}State', label, 0, '{:g}') for label, lamp in PfiLampsRow.lampNames]
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
        self.lamps = [LampState(self.moduleRow, lamp, label) for label, lamp in self.moduleRow.lampNames]

    def setInLayout(self):
        for i, lamp in enumerate(self.lamps):
            self.grid.addWidget(lamp, i // 3, i % 3)


class LampState(ValuesRow):
    def __init__(self, moduleRow, lampKey, lampLabel):
        widgets = [SwitchGB(moduleRow, f'{lampKey}State', '', 0, '{:d}'),
                   ValueGB(moduleRow, f'{lampKey}State', 'Volts', 1, '{:g}')]

        ValuesRow.__init__(self, widgets, title=lampLabel)
        self.grid.setContentsMargins(2, 8, 2, 2)


class PfiLampsCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)

        self.allStatus = CmdButton(controlPanel=controlPanel, label='ALL STATUS', cmdStr='pfilamps allstat')
        self.grid.addWidget(self.allStatus, 1, 0)
