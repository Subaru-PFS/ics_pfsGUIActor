__author__ = 'alefur'


from pfsGUIActor.control import ControlDialog
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.sps.lightSource import LightSourcePanel
from pfsGUIActor.sps.spec import SpecLabel

from pfsGUIActor.widgets import ValueMRow, ValueGB



class SpecModuleRow(ModuleRow):
    def __init__(self, spsModule, smId):
        ModuleRow.__init__(self, module=spsModule, actorName='sps', actorLabel='SPS')
        self.smId = smId
        self.specLabel = SpecLabel(self, smId)
        self.lightSource = ValueMRow(self, f'sm{smId}LightSource', 'Light Source', 0, '{:s}')

        self.createDialog(SpsDialog(self))

    @property
    def widgets(self):
        return [self.specLabel, self.lightSource]


class SpsDialog(ControlDialog):
    def __init__(self, spsRow):
        ControlDialog.__init__(self, moduleRow=spsRow, title='SPS')

        self.lightSource = LightSourcePanel(self)
        self.tabWidget.addTab(self.lightSource, 'Light Source')
