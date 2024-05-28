__author__ = 'alefur'

from pfsGUIActor.control import ControllerPanel, ControllerCmd
from pfsGUIActor.widgets import ValueGB


class RouterStatus(ValueGB):
    def __init__(self, controllerPanel):
        self.controllerPanel = controllerPanel
        ValueGB.__init__(self, controllerPanel.moduleRow, 'pfi_status', 'Router', 0, '{:s}')

    def setText(self, txt):
        isOnline = 'online' in txt
        txt = 'ONLINE' if isOnline else 'OFFLINE'
        self.controllerPanel.updateStatusIcon(isOnline)

        self.value.setText(txt)
        self.customize()


class PfiPanel(ControllerPanel):

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'pfi')
        self.addCommandSet(PfiCommands(self))

    def createWidgets(self):
        self.routerStatus = RouterStatus(self)

    def setInLayout(self):
        self.grid.addWidget(self.routerStatus, 0, 0)


class PfiCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
