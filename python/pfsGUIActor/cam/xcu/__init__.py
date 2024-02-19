__author__ = 'alefur'
addEng = False

import pfsGUIActor.styles as styles
from pfsGUIActor.cam.xcu.cooler import CoolerPanel
from pfsGUIActor.cam.xcu.gatevalve import GVPanel
from pfsGUIActor.cam.xcu.gauge import GaugePanel
from pfsGUIActor.cam.xcu.heaters import HeatersPanel
from pfsGUIActor.cam.xcu.interlock import InterlockPanel
from pfsGUIActor.cam.xcu.ionpump import IonpumpPanel
from pfsGUIActor.cam.xcu.motors import MotorsPanel
from pfsGUIActor.cam.xcu.pcm import PcmPanel
from pfsGUIActor.cam.xcu.temps import TempsPanel
from pfsGUIActor.cam.xcu.turbo import TurboPanel
from pfsGUIActor.common import ComboBox, GridLayout
from pfsGUIActor.control import ControlDialog, MultiplePanel, Topbar
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.widgets import Controllers, ValueMRow, CmdButton, CustomedCmd, SwitchMRow, SwitchGB, \
    ScientificNRow


class SetButton(CmdButton):
    def __init__(self, upperCmd):
        self.upperCmd = upperCmd
        CmdButton.__init__(self, controlPanel=None, controlDialog=upperCmd.controlDialog, label='SET cryoMode')

    def buildCmd(self):
        return self.upperCmd.buildCmd()


class SetCryoMode(CustomedCmd):
    validModes = ('offline', 'roughing', 'pumpdown', 'ionpumping', 'cooldown', 'operation', 'warmup', 'bakeout')

    def __init__(self, controlDialog):
        GridLayout.__init__(self)
        self.controlDialog = controlDialog
        self.button = SetButton(self)

        self.combo = ComboBox()
        self.combo.addItems(list(SetCryoMode.validModes))

        self.addWidget(self.button, 0, 0)
        self.addWidget(self.combo, 0, 1)

    def buildCmd(self):
        cmdStr = '%s setCryoMode %s ' % (self.controlDialog.moduleRow.actorName, self.combo.currentText())
        return cmdStr


class PidTemp(ValueMRow):
    tempChannels = dict(asic=9, h4=11, ccd=11)
    heaterNumbers = dict(asic=1, h4=2, ccd=2)

    def __init__(self, moduleRow, tempName):
        self.tempName = tempName
        tempChannel = self.tempChannels[tempName]
        heaterNumber = self.heaterNumbers[tempName]
        ValueMRow.__init__(self, moduleRow, 'temps', f'{tempName.upper()} Temp(K)', tempChannel, '{:.1f}',
                           controllerName='temps')

        heaterKey = f'heater{heaterNumber}'

        self.mode = ValueMRow(moduleRow, heaterKey, 'mode', 1, '{:s}')
        self.setpoint = ValueMRow(moduleRow, heaterKey, 'setpoint', 2, '{:.1f}')

    def setText(self, txt):
        mode = self.mode.value.text()

        if mode == 'TEMP':
            txt = f'{self.setpoint.value.text()}|{txt}'

        ValueMRow.setText(self, txt)

    def getStyles(self, text):
        mode = self.mode.value.text()

        if mode == 'TEMP':
            state = 'online'
            self.setTitle(f'{self.tempName.upper()}(K) LOOP ON')
        else:
            state = 'default'
            self.setTitle(f'{self.tempName.upper()} Temp(K)')

        background, police = styles.colorWidget(state)

        return background, police


class SingleIonPump(SwitchGB):
    def __init__(self, twoIonPumps, *args, **kwargs):
        self.twoIonPumps = twoIonPumps
        SwitchGB.__init__(self, twoIonPumps.moduleRow, *args, **kwargs)

    def setText(self, txt):
        SwitchGB.setText(self, txt)
        self.twoIonPumps.setText(txt)


class TwoIonPumps(SwitchMRow):
    def __init__(self, moduleRow):
        SwitchMRow.__init__(self, moduleRow, 'ionpump1', 'Ion Pumps', 0, '{:g}')
        self.ionpump1 = SingleIonPump(self, 'ionpump1', 'state', 0, '{:g}')
        self.ionpump2 = SingleIonPump(self, 'ionpump2', 'state', 0, '{:g}')

    def setText(self, txt):
        try:
            ionpump1 = self.ionpump1.value.text()
            ionpump2 = self.ionpump2.value.text()

            if ionpump1 == 'nan' or ionpump2 == 'nan':
                raise ValueError
            sums = int(ionpump1 == 'OFF') + int(ionpump2 == 'OFF')
            if sums == 0:
                txt = "ON"
            elif sums == 2:
                txt = "OFF"
            else:
                raise ValueError
        except ValueError:
            txt = "undef"

        self.value.setText(txt)
        self.customize()


class XcuRow(ModuleRow):
    tempNames = dict(b=['ccd'], r=['ccd'], n=['h4', 'asic'])

    def __init__(self, camRow):
        self.camRow = camRow
        ModuleRow.__init__(self, module=camRow.module,
                           actorName='xcu_%s%i' % (camRow.arm, camRow.module.specNum), actorLabel='XCU')

        self.cryoMode = ValueMRow(self, 'cryoMode', 'cryoMode', 0, '{:s}', controllerName='')
        self.temps = [PidTemp(self, tempName) for tempName in self.tempNames[camRow.arm]]
        self.pressure = ScientificNRow(self, 'pressure', 'Pressure(Torr)', 0, '{:.5e}', controllerName='PCM')
        self.twoIonPumps = TwoIonPumps(self)
        self.controllers = Controllers(self)
        self.actorStatus.button.setEnabled(False)

    @property
    def widgets(self):
        return [self.cryoMode, self.pressure, self.twoIonPumps] + self.temps

    def setOnline(self):
        ModuleRow.setOnline(self)
        self.camRow.setOnline()

    def createDialog(self, tabWidget):
        self.controlDialog = XcuDialog(self, tabWidget)


class XcuDialog(ControlDialog):
    def __init__(self, xcuRow, tabWidget):
        self.moduleRow = xcuRow
        self.tabWidget = tabWidget

        self.topbar = Topbar(self)
        self.setCryoMode = SetCryoMode(self)
        self.topbar.insertWidget(0, self.moduleRow.actorStatus)

        self.topbar.addLayout(self.setCryoMode)

        self.pcmPanel = PcmPanel(self)
        self.motorsPanel = MotorsPanel(self)

        self.GVPanel = GVPanel(self)
        self.interlockPanel = InterlockPanel(self)
        self.turboPanel = TurboPanel(self)
        self.ionpumpPanel = IonpumpPanel(self)
        self.gaugePanel = GaugePanel(self)

        self.coolerPanels = [CoolerPanel(self), CoolerPanel(self, 'cooler2')] if self.isNir else [CoolerPanel(self)]
        self.tempsPanel = TempsPanel(self)
        self.heatersPanel = HeatersPanel(self)

        vacuumPanel = MultiplePanel(self)
        coolingPanel = MultiplePanel(self)

        vacuumPanel.addWidget(self.GVPanel, 0, 0, 1, 3)
        vacuumPanel.addWidget(self.interlockPanel, 1, 0, 1, 2)
        vacuumPanel.addWidget(self.gaugePanel, 1, 2)
        vacuumPanel.addWidget(self.turboPanel, 2, 0, 1, 3)
        vacuumPanel.addWidget(self.ionpumpPanel, 3, 0, 1, 3)

        for i, cooler in enumerate(self.coolerPanels):
            coolingPanel.addWidget(cooler, i, 0)

        coolingPanel.addWidget(self.tempsPanel, i + 1, 0)
        # coolingPanel.addWidget(self.heatersPanel, i + 2, 0)

        self.tabWidget.addTab(self.pcmPanel, 'PCM')
        self.tabWidget.addTab(self.motorsPanel, 'Motors')

        self.tabWidget.addTab(vacuumPanel, 'Pumping / Vacuum')
        self.tabWidget.addTab(coolingPanel, 'Cooling')
        self.tabWidget.addTab(self.heatersPanel, 'Heaters')

    @property
    def cmdBuffer(self):
        return self.moduleRow.camRow.controlDialog.cmdBuffer

    @property
    def pannels(self):
        return [self.pcmPanel, self.motorsPanel, self.GVPanel, self.interlockPanel, self.turboPanel, self.ionpumpPanel,
                self.gaugePanel, self.tempsPanel, self.heatersPanel] + self.coolerPanels

    @property
    def isNir(self):
        return self.moduleRow.camRow.isNir
