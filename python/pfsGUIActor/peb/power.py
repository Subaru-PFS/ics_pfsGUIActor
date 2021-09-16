__author__ = 'alefur'

from pfsGUIActor.common import ComboBox
from pfsGUIActor.control import ControllerPanel, ControllerCmd
from pfsGUIActor.enu import EnuDeviceCmd
from pfsGUIActor.widgets import ValueGB, CustomedCmd, CmdButton, ValuesRow


class PowerPanel(ControllerPanel):

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'power')
        self.addCommandSet(PowerCommands(self))

    def createWidgets(self):
        pass

        # Key('power',
        #     Int(name='AGC_1', units='V'),
        #     Int(name='AGC_2', units='V'),
        #     Int(name='AGC_3', units='V'),
        #     Int(name='AGC_4', units='V'),
        #     Int(name='AGC_5', units='V'),
        #     Int(name='AGC_6', units='V'),
        #     Int(name='Leakage', units='V'),
        #     Int(name='Adam6015', units='V'),
        #     Int(name='USB_1', units='V'),
        #     Int(name='USB_2', units='V'),
        #     Int(name='Flow_board', units='V'),
        #     Int(name='LED_board', units='V'),
        #     Int(name='Switch', units='V'),

    def setInLayout(self):
        pass


class PowerCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
