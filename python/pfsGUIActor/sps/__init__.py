__author__ = 'alefur'

from pfsGUIActor.control import ControlDialog
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.sps.lightSource import LightSourcePanel
from pfsGUIActor.sps.spec import SpecLabel
from pfsGUIActor.widgets import ValueMRow


class SpecModuleRow(ModuleRow):
    def __init__(self, spsModule):
        ModuleRow.__init__(self, module=spsModule, actorName='sps', actorLabel='SPS')

        self.specLabels = [SpecLabel(self, specNum) for specNum in range(1, 5)]

        self.createDialog(SpsDialog(self))

    @property
    def widgets(self):
        return self.specLabels


class SpsDialog(ControlDialog):
    def __init__(self, spsRow):
        ControlDialog.__init__(self, moduleRow=spsRow, title='SPS')

        self.lightSource = LightSourcePanel(self)
        self.tabWidget.addTab(self.lightSource, 'Light Source')
