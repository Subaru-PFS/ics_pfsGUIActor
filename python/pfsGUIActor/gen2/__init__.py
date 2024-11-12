__author__ = 'alefur'

from pfsGUIActor.control import ControlDialog
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.widgets import ValueMRow, SwitchMRow


class Gen2Row(ModuleRow):
    def __init__(self, module):
        ModuleRow.__init__(self, module=module, actorName='gen2', actorLabel='GEN2')

        self.domeShutter = ValueMRow(self, 'domeShutter', 'Dome Shutter', 0, '{:s}')
        self.domeLight = SwitchMRow(self, 'domeLights', 'Dome Lights', 0, '{:d}')
        self.topScreenPos = ValueMRow(self, 'topScreenPos', 'Top Screen Position', 2, '{:s}')

        self.createDialog(Gen2Dialog(self))

    @property
    def widgets(self):
        return [self.domeShutter, self.domeLight, self.topScreenPos]


class Gen2Dialog(ControlDialog):
    def __init__(self, gen2Row):
        ControlDialog.__init__(self, moduleRow=gen2Row)
