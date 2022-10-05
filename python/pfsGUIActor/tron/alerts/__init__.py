__author__ = 'alefur'

from pfsGUIActor.control import ControlDialog
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.widgets import Controllers, ValueMRow


class AlertsRow(ModuleRow):
    def __init__(self, module):
        ModuleRow.__init__(self, module=module, actorName='alerts', actorLabel='')

        self.status = ValueMRow(self, 'alertStatus', 'ALERTS', 0, '{:s}')

        self.status.grid.addWidget(self.actorStatus.button, 0, 0)
        self.controllers = Controllers(self)
        self.createDialog(AlertsDialog(self))

    @property
    def widgets(self):
        return [self.status]


class AlertsDialog(ControlDialog):
    def __init__(self, alertsRow):
        ControlDialog.__init__(self, moduleRow=alertsRow)