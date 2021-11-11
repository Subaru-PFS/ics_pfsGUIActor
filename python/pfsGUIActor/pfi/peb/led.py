__author__ = 'alefur'

import pfsGUIActor.styles as styles
from pfsGUIActor.common import ComboBox
from pfsGUIActor.control import ControllerPanel, ControllerCmd
from pfsGUIActor.enu import EnuDeviceCmd
from pfsGUIActor.widgets import ValueGB, CustomedCmd, CmdButton, ValuesRow, SpinBoxGB


class LedWidget(ValuesRow):
    def __init__(self, moduleRow, ledName, index):
        widgets = [ValueGB(moduleRow, 'ledperiod', 'ledPeriod(uS)', index, '{:g}'),
                   ValueGB(moduleRow, 'dutycycle', 'dutyCycle(%)', index, '{:g}')]

        ValuesRow.__init__(self, widgets, title=ledName)
        self.grid.setContentsMargins(1, 6, 1, 1)


class DutyCycle(ValueGB):
    def __init__(self, moduleRow):
        ValueGB.__init__(self, moduleRow, 'dutycycle', 'dutyCycle(%)', 0, '{:g}')

    def customize(self):
        state = 'on' if float(self.value.text()) > 0 else 'off'
        background, police = styles.colorWidget(state)

        self.setColor(background=background, police=police)
        self.setEnabled(self.moduleRow.isOnline)


class LedNowWidget(ValuesRow):
    def __init__(self, moduleRow):
        widgets = [ValueGB(moduleRow, 'ledperiod', 'ledPeriod(uS)', 0, '{:g}'),
                   DutyCycle(moduleRow)]

        ValuesRow.__init__(self, widgets, title='Now')
        self.grid.setContentsMargins(1, 6, 1, 1)


class LedPowerCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SET POWER')

        self.state = ComboBox()
        self.state.addItems(['ON', 'OFF', 'FLASH'])
        self.addWidget(self.state, 0, 1)

    def buildCmd(self):
        cmdStr = '%s led %s' % (self.controlPanel.actorName, self.state.currentText().lower())
        return cmdStr


class Period(ValueGB):
    def __init__(self, config):
        self.spinbox = SpinBoxGB('Period', 0, 1000000)
        ValueGB.__init__(self, config.controlPanel.moduleRow, 'ledperiod', '', config.index, '{:g}')

    def setText(self, txt):
        if not self.spinbox.locked:
            self.spinbox.setValue(txt)

    def getValue(self):
        return self.spinbox.getValue()


class Duty(ValueGB):
    def __init__(self, config):
        self.spinbox = SpinBoxGB('Duty', 0, 100)
        ValueGB.__init__(self, config.controlPanel.moduleRow, 'dutycycle', '', config.index, '{:g}')

    def setText(self, txt):
        if not self.spinbox.locked:
            self.spinbox.setValue(float(txt))


    def getValue(self):
        return self.spinbox.getValue()


class SetConfigCmd(CustomedCmd):
    cmdHead = dict(on='config', flash='configflash')
    indexes = dict(on=1, flash=2)

    def __init__(self, controlPanel, mode):
        self.mode = mode
        self.index = self.indexes[mode]
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel=f'SET {self.mode.upper()} CONFIG')

        self.period = Period(self)
        self.duty = Duty(self)

        self.addWidget(self.period.spinbox, 0, 1)
        self.addWidget(self.duty.spinbox, 0, 2)

    def buildCmd(self):
        cmdStr = f'{self.controlPanel.actorName} led {self.cmdHead[self.mode]} ledperiod={self.period.getValue()} ' \
                 f'dutycycle={self.duty.getValue()}'

        return cmdStr


class LedPanel(ControllerPanel):

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'led')
        self.addCommandSet(LedCommands(self))

    def createWidgets(self):
        self.ledNow = LedNowWidget(self.moduleRow)
        self.ledOn = LedWidget(self.moduleRow, 'Config (ON)', 1)
        self.ledFlash = LedWidget(self.moduleRow, 'Config (FLASH)', 2)

    def setInLayout(self):
        self.grid.addWidget(self.ledNow, 0, 0, 1, 2)
        self.grid.addWidget(self.ledOn, 1, 0, 1, 2)
        self.grid.addWidget(self.ledFlash, 2, 0, 1, 2)


class LedCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)

        self.ledPowerCmd = LedPowerCmd(controlPanel=controlPanel)
        self.ledOnConfigCmd = SetConfigCmd(controlPanel=controlPanel, mode='on')
        self.ledFlashConfigCmd = SetConfigCmd(controlPanel=controlPanel, mode='flash')
        self.grid.addLayout(self.ledPowerCmd, 1, 0, 1, 2)
        self.grid.addLayout(self.ledOnConfigCmd, 2, 0, 1, 2)
        self.grid.addLayout(self.ledFlashConfigCmd, 3, 0, 1, 2)
