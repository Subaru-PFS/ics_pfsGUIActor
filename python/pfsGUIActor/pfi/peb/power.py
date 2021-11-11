__author__ = 'alefur'

from pfsGUIActor.common import ComboBox
from pfsGUIActor.control import ControllerPanel, ControllerCmd
from pfsGUIActor.enu import EnuDeviceCmd
from pfsGUIActor.widgets import ValueGB, CustomedCmd, CmdButton, ValuesRow, SwitchGB, SwitchButton


class SwitchPEB(SwitchButton):
    def __init__(self, controlPanel, identifier):
        cmdStrOn = f'{controlPanel.actorName} power on {identifier.outletId}'
        cmdStrOff = f'{controlPanel.actorName} power off {identifier.outletId}'
        SwitchButton.__init__(self, controlPanel=controlPanel, key='power', ind=identifier.keyId,
                              label=identifier.outletName, fmt='{:d}', cmdHead='', cmdStrOn=cmdStrOn,
                              cmdStrOff=cmdStrOff)


class BouncePEB(SwitchButton):
    def __init__(self, controlPanel, identifier):
        cmdStrOn = f'{controlPanel.actorName} power bounce {identifier.outletId}'
        cmdStrOff = f'{controlPanel.actorName} power bounce {identifier.outletId}'
        SwitchButton.__init__(self, controlPanel=controlPanel, key='power', ind=identifier.keyId,
                              label=identifier.outletName, labelOn='BOUNCE', labelOff='BOUNCE',
                              fmt='{:d}', cmdHead='', cmdStrOn=cmdStrOn, cmdStrOff=cmdStrOff)


class PebSwitchIdentifier(object):
    def __init__(self, outletName, keyId, outletId):
        self.outletName = outletName
        self.keyId = keyId
        self.outletId = outletId


class AGCIdentifier(PebSwitchIdentifier):
    def __init__(self, agcId):
        PebSwitchIdentifier.__init__(self, f'AGC {agcId}', agcId - 1, f'agc id={agcId}')


class PowerPanel(ControllerPanel):
    switches = [AGCIdentifier(i + 1) for i in range(6)] + \
               [PebSwitchIdentifier('Leakage', 6, 'leakage')] + [PebSwitchIdentifier('Adam6015', 7, 'adam')] + \
               [PebSwitchIdentifier('USB_1', 10, 'usb ids=1')] + [PebSwitchIdentifier('USB_2', 11, 'usb ids=2')]

    bounces = [PebSwitchIdentifier('Flow Board', 8, 'boardb')] + [PebSwitchIdentifier('Led Board', 9, 'boardc')] + \
              [PebSwitchIdentifier('Switch', 12, 'switch')]

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'power')
        self.addCommandSet(PowerCommands(self))

    def createWidgets(self):
        self.outlets = [SwitchGB(self.moduleRow, 'power', identifier.outletName, identifier.keyId, '{:d}')
                        for identifier in PowerPanel.switches + PowerPanel.bounces]

    def setInLayout(self):
        for i, value in enumerate(self.outlets):
            self.grid.addWidget(value, i // 3, i % 3)


class PowerCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)

        for i, identifier in enumerate(controlPanel.switches):
            self.grid.addWidget(SwitchPEB(controlPanel, identifier), 1 + i // 3, i % 3)

        for j, identifier in enumerate(controlPanel.bounces):
            j += (i + 1)
            self.grid.addWidget(BouncePEB(controlPanel, identifier), 1 + j // 3, j % 3)
