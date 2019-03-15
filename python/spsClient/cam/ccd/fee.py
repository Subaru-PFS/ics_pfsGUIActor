__author__ = 'alefur'
from spsClient.control import ControllerPanel, ControllerCmd
from spsClient.widgets import ValueGB


class FeePanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'fee')
        self.addCommandSet(FeeCommands(self))

    def createWidgets(self):
        self.preamp = ValueGB(self.moduleRow, 'ccdTemps', 'Preamp', 0, '{:.2f}')
        self.ccd0 = ValueGB(self.moduleRow, 'ccdTemps', 'Ccd0', 1, '{:.2f}')
        self.ccd1 = ValueGB(self.moduleRow, 'ccdTemps', 'Ccd1', 2, '{:.2f}')

    def setInLayout(self):
        self.grid.addWidget(self.preamp, 0, 0)
        self.grid.addWidget(self.ccd0, 0, 1)
        self.grid.addWidget(self.ccd1, 0, 2)


class FeeCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
