__author__ = 'alefur'

from pfsGUIActor.common import ComboBox
from pfsGUIActor.control import ControllerPanel, ControllerCmd
from pfsGUIActor.enu import EnuDeviceCmd
from pfsGUIActor.widgets import ValueGB, CustomedCmd, CmdButton, ValuesRow


class TempsPanel(ControllerPanel):
    probeNames = ['AGC 4', 'AGC 3', 'AGC 2', 'AGC 1', 'AGC 6', 'AGC 5', 'UL link 1', 'UL link 2', 'UL link 3',
                  'Positioner Frame', 'COB 1', 'COB 2', 'COB 3', 'COB 4', 'COB 5', 'COB 6', 'Ebox 1', 'Ebox 2',
                  'Ebox 3', 'Flow in', 'Flow out']

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'temps')
        self.addCommandSet(TempsCommands(self))

    def createWidgets(self):
        probeIndexes = [(i, name) for i, name in zip(list(range(len(self.probeNames))), self.probeNames)]
        probeIndexes.sort(key=lambda tup: tup[1])

        self.temps = [ValueGB(self.moduleRow, 'temps', f'{probeName}(°C)', index, '{:g}') for index, probeName in
                      probeIndexes]

    def setInLayout(self):
        for i, value in enumerate(self.temps):
            self.grid.addWidget(value, i // 6, i % 6)


class TempsCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
