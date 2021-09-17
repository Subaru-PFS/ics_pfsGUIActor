__author__ = 'alefur'

from pfsGUIActor.common import ComboBox
from pfsGUIActor.control import ControllerPanel, ControllerCmd
from pfsGUIActor.enu import EnuDeviceCmd
from pfsGUIActor.widgets import ValueGB, CustomedCmd, CmdButton, ValuesRow, SwitchGB, SwitchButton


class SwitchPEB(SwitchButton):
    def __init__(self, controlPanel, label, ind, identifier):
        cmdStrOn = f'{controlPanel.actorName} power on {identifier}'
        cmdStrOff = f'{controlPanel.actorName} power off {identifier}'
        SwitchButton.__init__(self, controlPanel=controlPanel, key='power', ind=ind, label=label, fmt='{:d}',
                              cmdHead='', cmdStrOn=cmdStrOn, cmdStrOff=cmdStrOff)


class SwitchAGC(SwitchPEB):
    def __init__(self, controlPanel, agcId):
        SwitchPEB.__init__(self, controlPanel, f'AGC {agcId}', agcId - 1, f'agc ids={agcId}')


class PowerPanel(ControllerPanel):
    outletsNames = ['AGC 1', 'AGC 2', 'AGC 3', 'AGC 4', 'AGC 5', 'AGC 6', 'Leakage', 'Adam6015', 'USB 1', 'USB 2',
                    'Flow board', 'LED board', 'Switch']

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'power')
        self.addCommandSet(PowerCommands(self))

    def createWidgets(self):
        self.outlets = [SwitchGB(self.moduleRow, 'power', outlet, index, '{:d}') for index, outlet in
                        enumerate(self.outletsNames)]

    def setInLayout(self):
        for i, value in enumerate(self.outlets):
            self.grid.addWidget(value, i // 3, i % 3)


class PowerCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)

        for i in range(6):
            self.grid.addWidget(SwitchAGC(controlPanel, agcId=i + 1), 1 + i // 3, i % 3)
        #
        for label, ind, identifier in [('Leakage', 6, 'leakage'), ('Adam6015', 7, 'adam'), ('USB-1', 10, 'usb ids=1'),
                                       ('USB-2', 11, 'usb ids=2')]:
            i+=1
            self.grid.addWidget(SwitchPEB(controlPanel, label, ind, identifier),   1 + i // 3, i % 3)

        for label, ind, identifier in [('Flow Board', 8, 'boardb'), ('LED Board', 9, 'boardc'), ('Switch', 12, 'switch')]:
            i += 1
            pass

