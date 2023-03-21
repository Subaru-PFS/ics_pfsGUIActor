__author__ = 'alefur'

from pfsGUIActor.control import ControllerPanel
from pfsGUIActor.enu import EnuDeviceCmd
from pfsGUIActor.widgets import ValueGB, CustomedCmd, SwitchGB, SpinBoxGB, SwitchButton


class BiaPower(ValueGB):
    def __init__(self, moduleRow):
        self.spinbox = SpinBoxGB('Power', 1, 100)
        ValueGB.__init__(self, moduleRow, 'biaStatus', '', 0, '{:d}')

    def setText(self, txt):
        if not self.spinbox.locked:
            self.spinbox.setValue(txt)

    def getValue(self):
        return self.spinbox.getValue()


class StrobePeriod(ValueGB):
    def __init__(self, moduleRow):
        self.spinbox = SpinBoxGB('Period', 10, 10000)
        ValueGB.__init__(self, moduleRow, 'biaStatus', '', 1, '{:d}')

    def setText(self, txt):
        if not self.spinbox.locked:
            self.spinbox.setValue(txt)

    def getValue(self):
        return self.spinbox.getValue()


class StrobeDuty(ValueGB):
    def __init__(self, moduleRow):
        self.spinbox = SpinBoxGB('Duty', 1, 100)
        ValueGB.__init__(self, moduleRow, 'biaStatus', '', 2, '{:d}')

    def setText(self, txt):
        if not self.spinbox.locked:
            self.spinbox.setValue(txt)

    def getValue(self):
        return self.spinbox.getValue()


class SetStrobeParamCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SET STROBE')

        self.period = StrobePeriod(moduleRow=self.controlPanel.moduleRow)
        self.duty = StrobeDuty(moduleRow=self.controlPanel.moduleRow)

        self.addWidget(self.period.spinbox, 0, 1)
        self.addWidget(self.duty.spinbox, 0, 2)

    def buildCmd(self):
        cmdStr = '%s bia period=%i duty=%i ' % (self.controlPanel.actorName, self.period.getValue(),
                                                self.duty.getValue())
        return cmdStr


class SetBiaPower(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SET POWER')

        self.power = BiaPower(moduleRow=self.controlPanel.moduleRow)

        self.addWidget(self.power.spinbox, 0, 1)

    def buildCmd(self):
        cmdStr = '%s bia power=%i' % (self.controlPanel.actorName, self.power.getValue())
        return cmdStr


class SwitchBia(SwitchButton):
    def __init__(self, controlPanel):
        SwitchButton.__init__(self, controlPanel=controlPanel, key='bia', label='BIA', fmt='{:s}',
                              cmdHead='%s bia' % controlPanel.actorName)

    def setText(self, txt):
        bool = True if txt in ['undef', 'on'] else False

        self.buttonOn.setVisible(not bool)
        self.buttonOff.setVisible(bool)


class BiaPanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'biasha')
        self.addCommandSet(BiaCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'biashaMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'biashaFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'biashaFSM', '', 1, '{:s}')

        self.bia = SwitchGB(self.moduleRow, 'bia', 'BIA', 0, '{:s}')
        self.biaStrobe = SwitchGB(self.moduleRow, 'biaConfig', 'Strobe', 0, '{:d}')
        self.biaPower = ValueGB(self.moduleRow, 'biaStatus', 'LED Power(%)', 0, '{:d}')

        self.biaPeriod = ValueGB(self.moduleRow, 'biaStatus', 'Period(ms)', 1, '{:d}')
        self.biaDuty = ValueGB(self.moduleRow, 'biaStatus', 'Duty(%)', 2, '{:d}')
        self.biaPulseOn = ValueGB(self.moduleRow, 'biaStatus', 'Pulse-On(ms)', 3, '{:d}')
        self.biaPulseOff = ValueGB(self.moduleRow, 'biaStatus', 'Pulse-Off(ms)', 4, '{:d}')

        self.photores1 = ValueGB(self.moduleRow, 'photores', 'PhotoRes1', 0, '{:d}')
        self.photores2 = ValueGB(self.moduleRow, 'photores', 'PhotoRes2', 1, '{:d}')

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.bia, 1, 0)
        self.grid.addWidget(self.biaStrobe, 1, 1)
        self.grid.addWidget(self.biaPower, 1, 2)

        self.grid.addWidget(self.biaPeriod, 2, 0)
        self.grid.addWidget(self.biaDuty, 2, 1)
        self.grid.addWidget(self.biaPulseOn, 2, 2)
        self.grid.addWidget(self.biaPulseOff, 2, 3)

        self.grid.addWidget(self.photores1, 3, 0)
        self.grid.addWidget(self.photores2, 3, 1)


class BiaCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)
        self.switchBia = SwitchBia(controlPanel=controlPanel)
        self.switchStrobe = SwitchButton(controlPanel=controlPanel, key='biaConfig', label='STROBE',
                                         cmdHead='%s bia strobe' % controlPanel.actorName)

        self.setBiaPower = SetBiaPower(controlPanel=controlPanel)
        self.setStrobeParam = SetStrobeParamCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.switchBia, 1, 0)
        self.grid.addWidget(self.switchStrobe, 1, 1)
        self.grid.addLayout(self.setBiaPower, 2, 0, 1, 2)
        self.grid.addLayout(self.setStrobeParam, 3, 0, 1, 3)
