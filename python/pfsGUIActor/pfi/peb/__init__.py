__author__ = 'alefur'

import pfsGUIActor.styles as styles
from pfsGUIActor.control import ControlDialog
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.pfi.peb.flow import FlowPanel
from pfsGUIActor.pfi.peb.led import LedPanel
from pfsGUIActor.pfi.peb.power import PowerPanel
from pfsGUIActor.pfi.peb.temps import TempsPanel
from pfsGUIActor.pfi.peb.pfi import PfiPanel
from pfsGUIActor.widgets import SwitchGB, ValueMRow, Controllers, \
    SwitchMRow


class RouterStatus(ValueMRow):
    def __init__(self, moduleRow):
        ValueMRow.__init__(self, moduleRow, 'pfi_status', 'Router', 0, '{:s}')

    def setText(self, txt):
        txt = 'ONLINE' if 'online' in txt else 'OFFLINE'
        self.value.setText(txt)
        self.customize()


class SingleAGC(SwitchGB):
    def __init__(self, agcPower, agcId):
        self.agcPower = agcPower
        SwitchGB.__init__(self, agcPower.moduleRow, 'power', 'state', agcId, '{:g}')

    def setText(self, txt):
        SwitchGB.setText(self, txt)
        self.agcPower.setText(txt)


class AGCPower(SwitchMRow):
    def __init__(self, moduleRow):
        SwitchMRow.__init__(self, moduleRow, 'power', 'AGC Power', 0, '{:g}')
        self.agcs = [SingleAGC(self, agcId) for agcId in range(6)]

    def setText(self, txt):
        try:
            [txt] = list(set([agc.value.text() for agc in self.agcs]))
        except ValueError:
            txt = "undef"

        self.value.setText(txt)
        self.customize()


class LedPower(ValueMRow):
    def __init__(self, moduleRow):
        ValueMRow.__init__(self, moduleRow, 'dutycycle', 'LED Power(%)', 0, '{:g}')

    def customize(self):
        state = 'on' if float(self.value.text()) > 0 else 'off'
        background, police = styles.colorWidget(state)

        self.setColor(background=background, police=police)
        self.setEnabled(self.moduleRow.isOnline)


class PebRow(ModuleRow):
    def __init__(self, module):
        ModuleRow.__init__(self, module=module, actorName='peb', actorLabel='PEB')

        self.routerStatus = RouterStatus(self)
        self.agcPower = AGCPower(self)
        self.ledPower = LedPower(self)

        self.controllers = Controllers(self)
        self.createDialog(PebDialog(self))

    @property
    def widgets(self):
        return [self.routerStatus, self.agcPower, self.ledPower]


class PebDialog(ControlDialog):
    def __init__(self, pebRow):
        ControlDialog.__init__(self, moduleRow=pebRow)
        self.flowPanel = FlowPanel(self)
        self.tempsPanel = TempsPanel(self)
        self.powerPanel = PowerPanel(self)
        self.ledPanel = LedPanel(self)
        self.pfiPanel = PfiPanel(self)

        # telemetryPanel = MultiplePanel(self)
        # telemetryPanel.addWidget(self.flowPanel, 0, 0, 1, 1)
        # telemetryPanel.addWidget(self.tempsPanel, 1, 0, 1, 1)

        self.tabWidget.addTab(self.powerPanel, 'Power')
        self.tabWidget.addTab(self.ledPanel, 'LED')
        self.tabWidget.addTab(self.flowPanel, 'FLow')
        self.tabWidget.addTab(self.tempsPanel, 'Temps')
        self.tabWidget.addTab(self.pfiPanel, 'Pfi')
    # self.tabWidget.addTab(telemetryPanel, 'Telemetry')

    # @property
    # def panels(self):
    #     return [self.flowPanel, self.tempsPanel, self.powerPanel, self.ledPanel]
    #
    #
