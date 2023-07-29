__author__ = 'alefur'

from pfsGUIActor.common import ComboBox
from pfsGUIActor.control import ControlPanel, CommandsGB
from pfsGUIActor.sps.spec import SpecLabel
from pfsGUIActor.widgets import ValueGB, CustomedCmd


class LightSource:
    def __init__(self, controlPanel, specNum):
        self.label = SpecLabel(controlPanel.moduleRow, specNum)
        self.lightSource = ValueGB(controlPanel.moduleRow, f'sm{specNum}LightSource', '', 0, '{:s}')


class DeclareLightSourceCmd(CustomedCmd):
    known = ['dcb', 'dcb2', 'sunss', 'pfi', 'none']

    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='DECLARE')

        self.comboLight = ComboBox()
        self.comboLight.addItems(DeclareLightSourceCmd.known)

        self.comboSM = ComboBox()
        self.comboSM.addItems(['SM1', 'SM2', 'SM3', 'SM4', 'SPS'])
        self.comboSM.setMinimumWidth(45)

        self.addWidget(self.comboSM, 0, 1)
        self.addWidget(self.comboLight, 0, 2)

    def buildCmd(self):
        identifier = f'' if self.comboSM.currentText() =='SPS' else f'{self.comboSM.currentText().lower()}='
        return f'sps declareLightSource {identifier}{self.comboLight.currentText()}'


class LightSourcePanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)
        self.addCommandSet(Commands(self))

    def createWidgets(self):
        for specNum in range(1, 5):
            self.lightSources = [LightSource(self, specNum) for specNum in range(1, 5)]

    def setInLayout(self):
        for i in range(4):
            self.grid.addWidget(self.lightSources[i].label, i, 0)
            self.grid.addWidget(self.lightSources[i].lightSource, i, 1)


class Commands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.declare = DeclareLightSourceCmd(controlPanel)
        self.grid.addLayout(self.declare, 1, 0)
