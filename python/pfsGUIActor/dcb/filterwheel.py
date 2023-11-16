__author__ = 'alefur'

from ics.utils.instdata import instconfig
from pfsGUIActor.common import ComboBox
from pfsGUIActor.control import ControllerPanel
from pfsGUIActor.enu import EnuDeviceCmd
from pfsGUIActor.widgets import ValueGB, CustomedCmd, CmdButton, ValuesRow, SwitchGB, SwitchButton


class Wheel(ValuesRow):
    def __init__(self, moduleRow, name):
        widgets = [ValueGB(moduleRow, f'{name}wheel', 'Position', 0, '{:d}'),
                   ValueGB(moduleRow, f'{name}wheel', 'Hole', 1, '{:s}')]

        ValuesRow.__init__(self, widgets, title=f'{name.capitalize()} Wheel')
        self.grid.setContentsMargins(1, 6, 1, 1)


class SetFilterwheel(CustomedCmd):

    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SET')

        dcbConfig = instconfig.InstConfig(controlPanel.actorName)
        self.lineHoles = dcbConfig['filterwheel']['lineHoles']
        self.qthHoles = dcbConfig['filterwheel']['qthHoles']

        self.comboWheel = ComboBox()
        self.comboWheel.addItems(['LINEWHEEL', 'QTHWHEEL'])

        self.comboLinePosition = ComboBox()
        self.comboQthPosition = ComboBox()

        self.comboLinePosition.addItems([f'{hole}' for hole in self.lineHoles])
        self.comboQthPosition.addItems([f'{hole}' for hole in self.qthHoles])

        self.addWidget(self.comboWheel, 0, 1)
        self.addWidget(self.comboLinePosition, 0, 2)
        self.addWidget(self.comboQthPosition, 0, 2)

        self.comboWheel.currentIndexChanged.connect(self.displayComboPosition)
        self.comboWheel.setCurrentIndex(1)
        self.comboWheel.setCurrentIndex(0)

    @property
    def comboPosition(self):
        return self.comboLinePosition if self.comboWheel.currentIndex() == 0 else self.comboQthPosition

    def displayComboPosition(self, index):
        line, qth = (True, False) if index == 0 else (False, True)
        self.comboLinePosition.setVisible(line)
        self.comboQthPosition.setVisible(qth)

    def buildCmd(self):
        return f'{self.controlPanel.actorName} set {self.comboWheel.currentText().lower()}={self.comboPosition.currentText()}'


class InitFilterwheel(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='INIT')

        self.comboWheel = ComboBox()
        self.comboWheel.addItems(['default (both)', 'LINEWHEEL', 'QTHWHEEL'])

        self.addWidget(self.comboWheel, 0, 1)

    def buildCmd(self):
        if self.comboWheel.currentIndex() == 0:
            return f'{self.controlPanel.actorName} filterwheel init'
        else:
            return f'{self.controlPanel.actorName} init {self.comboWheel.currentText().lower()}'


class SwitchFilterwheel(SwitchButton):
    def __init__(self, controlPanel):
        cmdStrOn = f'{controlPanel.actorName} power on filterwheel'
        cmdStrOff = f'{controlPanel.actorName} power off filterwheel'
        SwitchButton.__init__(self, controlPanel=controlPanel, key='filterwheel', label='Filterwheel',
                              cmdHead='', cmdStrOn=cmdStrOn, cmdStrOff=cmdStrOff, labelOn='POWER ON',
                              labelOff='POWER OFF')

        self.grid.removeWidget(self.buttonOn)
        self.grid.removeWidget(self.buttonOff)


class FilterwheelPanel(ControllerPanel):

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'filterwheel')
        self.addCommandSet(FilterwheelCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'filterwheelMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'filterwheelFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'filterwheelFSM', '', 1, '{:s}')

        self.power = SwitchGB(self.moduleRow, 'filterwheel', 'Filterwheel', 0, '{:g}')
        self.linewheel = Wheel(self.moduleRow, 'line')
        self.qthwheel = Wheel(self.moduleRow, 'qth')

        self.adc1 = ValueGB(self.moduleRow, 'adc', 'ADC channel 1', 0, '{:.4f}')
        self.adc2 = ValueGB(self.moduleRow, 'adc', 'ADC channel 2', 1, '{:.4f}')

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.power, 1, 0)

        self.grid.addWidget(self.linewheel, 2, 0, 1, 2)
        self.grid.addWidget(self.qthwheel, 3, 0, 1, 2)

        self.grid.addWidget(self.adc1, 4, 0)
        self.grid.addWidget(self.adc2, 4, 1)


class FilterwheelCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)
        self.setFilterwheel = SetFilterwheel(controlPanel=controlPanel)
        self.initFilterwheel = InitFilterwheel(controlPanel=controlPanel)
        self.adcCalib = CmdButton(controlPanel=controlPanel, label='ADC CALIB',
                                  cmdStr=f'{controlPanel.actorName} adc calib')
        self.switchFilterwheel = SwitchFilterwheel(controlPanel)
        self.grid.addWidget(self.switchFilterwheel.buttonOn, 0, 2)
        self.grid.addWidget(self.switchFilterwheel.buttonOff, 0, 2)
        self.grid.addLayout(self.initFilterwheel, 1, 0, 1, 2)
        self.grid.addLayout(self.setFilterwheel, 2, 0, 1, 3)
        self.grid.addWidget(self.adcCalib, 3, 0, )
