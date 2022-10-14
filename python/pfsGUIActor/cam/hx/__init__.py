__author__ = 'alefur'

from pfsGUIActor.cam.hx.panel import HxPanel
from pfsGUIActor.control import ControlDialog, Topbar
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.widgets import Controllers, ValueMRow


class ExposureState(ValueMRow):
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        ValueMRow.__init__(self, moduleRow, 'exposureState', '', 0, '{:s}', controllerName='hxhal')

    def setText(self, txt):
        txt = txt.upper()
        ValueMRow.setText(self, txt)


class HxRow(ModuleRow):
    def __init__(self, camRow):
        self.camRow = camRow
        ModuleRow.__init__(self, module=camRow.module,
                           actorName='hx_%s%i' % (camRow.arm, camRow.module.smId), actorLabel='HX')

        self.controllers = Controllers(self)
        self.substate = ExposureState(self)
        self.actorStatus.button.setEnabled(False)

    @property
    def widgets(self):
        return [self.substate]

    def setOnline(self):
        ModuleRow.setOnline(self)
        self.camRow.setOnline()

    def createDialog(self, tabWidget):
        self.controlDialog = HxDialog(self, tabWidget)


class HxDialog(ControlDialog):
    def __init__(self, hxRow, tabWidget):
        self.moduleRow = hxRow
        self.tabWidget = tabWidget

        self.topbar = Topbar(self)
        self.topbar.insertWidget(0, self.moduleRow.actorStatus)

        self.hxPanel = HxPanel(self)
        self.tabWidget.addTab(self.hxPanel, 'hx')

    @property
    def cmdBuffer(self):
        return self.moduleRow.camRow.controlDialog.cmdBuffer

    @property
    def pannels(self):
        return [self.hxPanel]

