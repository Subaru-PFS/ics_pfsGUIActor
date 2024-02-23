__author__ = 'alefur'

from pfsGUIActor.cam import CamDevice
from pfsGUIActor.common import ComboBox
from pfsGUIActor.control import CommandsGB
from pfsGUIActor.widgets import SwitchGB, ValuesRow, ValueGB, CustomedCmd, CmdButton, SpinBoxGB, SwitchButton, \
    DoubleSpinBoxGB


class HeaterFraction(ValueGB):
    def __init__(self, moduleRow, heaterNb):
        ValueGB.__init__(self, moduleRow, 'heaters', 'power(%)', heaterNb + 2, '{:.2f}')

    def setText(self, txt):
        # Converting fraction to percentage.
        try:
            txt = '{:d}'.format(int(float(txt) * 100))
        except ValueError:
            txt = 'nan'

        self.value.setText(txt)
        self.customize()


class HeaterState(ValuesRow):
    def __init__(self, controlPanel, name):
        heaterNb = controlPanel.heaterChannels[name]
        self.name = name
        widgets = [SwitchGB(controlPanel.moduleRow, 'heaters', 'enabled', heaterNb, '{:g}'),
                   HeaterFraction(controlPanel.moduleRow, heaterNb)]

        ValuesRow.__init__(self, widgets, title=name.capitalize())


class PidHeaterState(ValueGB):
    def __init__(self, controlPanel, heaterKey):
        ValueGB.__init__(self, controlPanel.moduleRow, heaterKey, 'state', 4, '{:.2f}')

    def setText(self, text):
        def stateFromValue(text):
            value = float(text)
            text = 'ON' if value > 0 else 'OFF'
            return text

        text = stateFromValue(text) if text != 'nan' else text

        ValueGB.setText(self, text)


class PidHeaterStatus(ValuesRow):
    def __init__(self, controlPanel, heaterNumber, heaterName):
        self.name = heaterName
        heaterKey = f'heater{heaterNumber}'
        widgets = [PidHeaterState(controlPanel, heaterKey),
                   ValueGB(controlPanel.moduleRow, heaterKey, 'mode', 1, '{:s}'),
                   ValueGB(controlPanel.moduleRow, heaterKey, 'temp setPoint', 2, '{:.2f}'),
                   ValueGB(controlPanel.moduleRow, heaterKey, 'power setPoint', 3, '{:.2f}'),
                   ValueGB(controlPanel.moduleRow, heaterKey, 'fraction', 4, '{:.2f}'),
                   ValueGB(controlPanel.moduleRow, heaterKey, 'temp', 5, '{:.2f}'),
                   ]
        ValuesRow.__init__(self, widgets, title=heaterName.capitalize())


class HeatersPanel(CamDevice):
    hpHeaterNames = dict(b=['spreader'], r=['spreader'], n=['spreader', 'shield'])
    pidHeaterNames = dict(b=['', 'ccd'], r=['', 'ccd'], n=['asic', 'h4'])

    heaterChannels = dict(ccd=4, spreader=5, asic=0, shield=1, h4=4)

    def __init__(self, controlDialog):
        CamDevice.__init__(self, controlDialog, 'temps', 'Heaters')
        self.addCommandSet(HeatersCommands(self))

    def createWidgets(self):
        # sortedChannels = dict(sorted(self.heaterChannels.items(), key=lambda kv: kv[1])).keys()
        self.hpHeaters = [HeaterState(self, name) for name in self.hpHeaterNames[self.moduleRow.camRow.arm]]

        pidHeaters = []
        for i, name in enumerate(self.pidHeaterNames[self.moduleRow.camRow.arm]):
            if not name:
                continue
            pidHeaters.append(PidHeaterStatus(self, i + 1, name))

        self.pidHeaters = pidHeaters

    def setInLayout(self):
        for i, value in enumerate(self.hpHeaters):
            self.grid.addWidget(value, i, 0)

        for j, value in enumerate(self.pidHeaters):
            self.grid.addWidget(value, i + j + 1, 0)


class HPCmd(SwitchButton):

    def __init__(self, controlPanel, name):
        cmdStrOn = '%s HPheaters on %s' % (controlPanel.actorName, name)
        cmdStrOff = '%s HPheaters off %s' % (controlPanel.actorName, name)
        SwitchButton.__init__(self, controlPanel=controlPanel, key='heaters', label=name.capitalize(),
                              ind=controlPanel.heaterChannels[name], cmdHead='', cmdStrOn=cmdStrOn, cmdStrOff=cmdStrOff)

    def setText(self, txt):
        bool = True if txt.strip() in ['0', 'nan', 'off', 'undef'] else False
        self.buttonOn.setVisible(bool)
        self.buttonOff.setVisible(not bool)


class PidCmd(CustomedCmd):
    def __init__(self, controlPanel, name):
        self.name = name
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET %s' % name.upper())

        self.combo = ComboBox()
        self.combo.addItems(['TEMP', 'POWER'])
        self.combo.currentIndexChanged.connect(self.showMode)

        self.setpoint1 = DoubleSpinBoxGB('Temperature(K)', vmin=80, vmax=300, decimals=1)
        self.setpoint1.setValue(100)
        self.setpoint2 = SpinBoxGB('Power(percent)', vmin=0, vmax=100)

        self.setpoint2.hide()

        self.addWidget(self.combo, 0, 1)
        self.addWidget(self.setpoint1, 0, 2)
        self.addWidget(self.setpoint2, 0, 2)

    def buildCmd(self):
        setpoint = f'temp={self.setpoint1.getValue():.1f}' if not self.combo.currentIndex() else f'power={self.setpoint2.getValue():d}'
        return f'{self.controlPanel.actorName} heaters {self.name} {setpoint}'

    def showMode(self, index):
        if index == 0:
            self.setpoint1.show()
            self.setpoint2.hide()
        else:
            self.setpoint1.hide()
            self.setpoint2.show()


class HeatersCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s heaters status' % controlPanel.actorName)
        self.grid.addWidget(self.statusButton, 0, 0)

        for i, heater in enumerate(controlPanel.hpHeaters):
            self.grid.addWidget(HPCmd(controlPanel, heater.name), 1 + i, 0)

        for j, heater in enumerate(controlPanel.pidHeaters):
            self.grid.addLayout(PidCmd(controlPanel, heater.name), 2 + i + j, 0)
