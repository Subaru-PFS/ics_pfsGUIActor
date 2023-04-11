__author__ = 'alefur'

from pfsGUIActor.cam.xcu.gauge import GaugePanel
from pfsGUIActor.rough.pump import PumpPanel
from pfsGUIActor.control import ControlDialog, MultiplePanel
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.widgets import Controllers, ValueMRow, ScientificNRow


class RoughRow(ModuleRow):
    def __init__(self, spsModule, roughName):
        ModuleRow.__init__(self, module=spsModule, actorName=f'{roughName}', actorLabel=f'{roughName.upper()}')

        self.warning = ValueMRow(self, 'pumpWarnings', 'Warnings', 1, '{:s}', controllerName='pump')
        self.errors = ValueMRow(self, 'pumpErrors', 'Errors', 1, '{:s}', controllerName='pump')
        self.speed = ValueMRow(self, 'pumpSpeed', 'Speed', 0, '{:g}', controllerName='pump')
        self.pressure = ScientificNRow(self, 'pressure', 'Pressure(Torr)', 0, '{:.5e}', controllerName='gauge')

        self.controllers = Controllers(self)
        self.createDialog(RoughDialog(self))

    @property
    def widgets(self):
        return [self.warning, self.errors, self.speed, self.pressure]


class RoughDialog(ControlDialog):
    def __init__(self, roughRow):
        ControlDialog.__init__(self, moduleRow=roughRow)

        self.gaugePanel = GaugePanel(self, controllerName='gauge', label='Gauge', maxWidth=False)
        self.pumpPanel = PumpPanel(self)

        pumpPanel = MultiplePanel(self)
        pumpPanel.addWidget(self.gaugePanel, 0, 0)
        pumpPanel.addWidget(self.pumpPanel, 1, 0)

        self.tabWidget.addTab(pumpPanel, '')
        #self.tabWidget.addTab(self.pumpPanel, 'Pump')

    @property
    def pannels(self):
        return [self.gaugePanel, self.pumpPanel]
