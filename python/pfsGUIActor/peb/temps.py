__author__ = 'alefur'

from pfsGUIActor.common import ComboBox
from pfsGUIActor.control import ControllerPanel, ControllerCmd
from pfsGUIActor.enu import EnuDeviceCmd
from pfsGUIActor.widgets import ValueGB, CustomedCmd, CmdButton, ValuesRow


class TempsPanel(ControllerPanel):

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'temps')
        self.addCommandSet(TempsCommands(self))

    def createWidgets(self):
        pass
        # Float(name='AGC_4', units='degC'),
        # Float(name='AGC_3', units='degC'),
        # Float(name='AGC_2', units='degC'),
        # Float(name='AGC_1', units='degC'),
        # Float(name='AGC_6', units='degC'),
        # Float(name='AGC_5', units='degC'),
        # Float(name='UL_link_1', units='degC'),
        # Float(name='UL_link_2', units='degC'),
        # Float(name='UL_link_3', units='degC'),
        # Float(name='Positioner_frame', units='degC'),
        # Float(name='COB_1', units='degC'),
        # Float(name='COB_2', units='degC'),
        # Float(name='COB_3', units='degC'),
        # Float(name='COB_4', units='degC'),
        # Float(name='COB_5', units='degC'),
        # Float(name='COB_6', units='degC'),
        # Float(name='Ebox_1', units='degC'),
        # Float(name='Ebox_2', units='degC'),
        # Float(name='Ebox_3', units='degC'),
        # Float(name='Flow_in', units='degC'),
        # Float(name='Flow_out', units='degC'),
    def setInLayout(self):
        pass

class TempsCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
