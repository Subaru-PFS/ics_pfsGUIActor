__author__ = 'alefur'

from pfsGUIActor.cam import CamDevice
from pfsGUIActor.common import LineEdit
from pfsGUIActor.control import ControllerCmd
from pfsGUIActor.widgets import ValueGB, CustomedCmd


class Status(ValueGB):
    maxNb = 3
    def __init__(self, moduleRow):
        ValueGB.__init__(self, moduleRow, 'interlock', 'Status', 1, '{:s}')

    def setText(self, txt):
        ftext = [stat for stat in txt.split(',') if 'bit ' not in stat]
        chunks = [','.join(ftext[x:x + Status.maxNb]) for x in range(0, len(ftext), Status.maxNb)]

        self.value.setText('\n'.join(chunks))
        self.customize()


class InterlockPanel(CamDevice):
    def __init__(self, controlDialog):
        CamDevice.__init__(self, controlDialog, 'interlock')
        self.addCommandSet(InterlockCommands(self))

    def createWidgets(self):
        self.pCryostat = ValueGB(self.moduleRow, 'interlockPressures', 'pCryostat(Torr)', 0, '{:g}')
        self.pRoughing = ValueGB(self.moduleRow, 'interlockPressures', 'pRoughing(Torr)', 1, '{:g}')
        self.status = Status(self.moduleRow)

    def setInLayout(self):
        self.grid.addWidget(self.pCryostat, 0, 0)
        self.grid.addWidget(self.pRoughing, 0, 1)
        self.grid.addWidget(self.status, 1, 0, 3, 2)


class RawCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='RAW')

        self.rawCmd = LineEdit()
        self.addWidget(self.rawCmd, 0, 1)

    def buildCmd(self):
        cmdStr = '%s interlock raw=%s' % (self.controlPanel.actorName, self.rawCmd.text())
        return cmdStr


class InterlockCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
        self.rawCmd = RawCmd(controlPanel=controlPanel)
        self.grid.addLayout(self.rawCmd, 1, 0, 1, 2)
