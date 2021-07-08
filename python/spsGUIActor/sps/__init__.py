__author__ = 'alefur'


from spsGUIActor.control import ControlDialog
from spsGUIActor.modulerow import ModuleRow, RowWidget
from spsGUIActor.sps.lightSource import LightSourcePanel
from spsGUIActor.sps.spec import SpecLabel

from spsGUIActor.widgets import ValueMRow, ValueGB


class SpecModuleRow(RowWidget):
    def __init__(self, spsRow, smId):
        RowWidget.__init__(self, spsRow)
        self.smId = smId
        self.specLabel = SpecLabel(spsRow, smId)
        self.lightSource = ValueMRow(spsRow, f'sm{smId}LightSource', f'SM{smId} Light Source', 0, '{:s}')

    @property
    def widgets(self):
        return [self.lightSource]


# class SpecModuleRow(ModuleRow):
#     def __init__(self, spsModule, smId):
#         ModuleRow.__init__(self, module=spsModule, actorName='sps', actorLabel='SPS')
#         self.smId = smId
#         self.specLabel = SpecLabel(self, smId)
#         self.lightSource = ValueMRow(self, f'sm{smId}LightSource', 'Light Source', 0, '{:s}')
#
#         self.createDialog(SpsDialog(self))
#
#     @property
#     def widgets(self):
#         return [self.specLabel, self.lightSource]
#

class SpsDialog(ControlDialog):
    def __init__(self, spsRow):
        ControlDialog.__init__(self, moduleRow=spsRow, title='SPS')

        self.lightSource = LightSourcePanel(self)
        self.tabWidget.addTab(self.lightSource, 'Light Source')


class SpsRow(ModuleRow):
    def __init__(self, spsModule):
        ModuleRow.__init__(self, module=spsModule, actorName='sps', actorLabel='SPS')
        self.smRows = dict([(smId, SpecModuleRow(self, smId)) for smId in spsModule.mwindow.smIds])

        self.createDialog(SpsDialog(self))

    @property
    def widgets(self):
        return sum([row.widgets for row in self.smRows.values()], [])