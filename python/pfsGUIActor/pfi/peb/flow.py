__author__ = 'alefur'

from pfsGUIActor.common import ComboBox
from pfsGUIActor.control import ControllerPanel, ControllerCmd
from pfsGUIActor.enu import EnuDeviceCmd
from pfsGUIActor.widgets import ValueGB, CustomedCmd, CmdButton, ValuesRow


class LeakageBox(ValueGB):
    def setText(self, txt):
        try:
            txt = 'ALARM' if not int(txt) else 'OK'
        except ValueError:
            pass
        ValueGB.setText(self, txt)


class FlowPanel(ControllerPanel):

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'flow')
        self.addCommandSet(FlowCommands(self))

    def createWidgets(self):
        self.humidity = ValueGB(self.moduleRow, 'humidity', 'Humidity(%)', 0, '{:g}')
        self.temp = ValueGB(self.moduleRow, 'humidity', 'Temperature(°C)', 1, '{:g}')
        self.dewpoint = ValueGB(self.moduleRow, 'humidity', 'Dew Point(°C)', 2, '{:g}')

        self.flowMeter = ValueGB(self.moduleRow, 'flow', 'Flow Meter(Gal/min)', 0, '{:g}')
        self.flowRotor = ValueGB(self.moduleRow, 'flow', 'Flow Rotor(Hz)', 1, '{:g}')

        self.leakage = LeakageBox(self.moduleRow, 'leakage', 'Leakage', 0, '{:g}')
        self.disconnect = LeakageBox(self.moduleRow, 'leakage', 'Disconnect', 1, '{:g}')

    def setInLayout(self):
        self.grid.addWidget(self.humidity, 0, 0)
        self.grid.addWidget(self.temp, 0, 1)
        self.grid.addWidget(self.dewpoint, 0, 2)

        self.grid.addWidget(self.flowMeter, 1, 0)
        self.grid.addWidget(self.flowRotor, 1, 1)

        self.grid.addWidget(self.leakage, 2, 0)
        self.grid.addWidget(self.disconnect, 2, 1)


class FlowCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
