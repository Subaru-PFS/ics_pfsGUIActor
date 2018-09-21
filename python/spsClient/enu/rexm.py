__author__ = 'alefur'
from PyQt5.QtWidgets import QComboBox
from spsClient.widgets import ValueGB, ControlPanel, CmdButton, CustomedCmd, CommandsGB, AbortButton


class MoveCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='MOVE')

        self.combo = QComboBox()
        self.combo.addItems(['low', 'mid'])

        self.addWidget(self.combo, 0, 1)

    def buildCmd(self):
        cmdStr = '%s rexm move %s ' % (self.controlPanel.actorName, self.combo.currentText())

        return cmdStr


class RexmCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s rexm status' % controlPanel.actorName)
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='%s connect controller=rexm' % controlPanel.actorName)
        self.initButton = CmdButton(controlPanel=controlPanel, label='INIT',
                                    cmdStr='%s rexm init' % controlPanel.actorName)
        self.abortButton = AbortButton(controlPanel=controlPanel, cmdStr='%s rexm abort' % controlPanel.actorName)

        self.moveCmd = MoveCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)
        self.grid.addWidget(self.initButton, 1, 0)
        self.grid.addWidget(self.abortButton, 1, 1)
        self.grid.addLayout(self.moveCmd, 2, 0, 1, 2)
        #self.grid.addWidget(self.empty, 3, 0, 1, 3)

    @property
    def buttons(self):
        return [self.statusButton, self.connectButton, self.initButton, self.abortButton, self.moveCmd.button]


class RexmPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.mode = ValueGB(self.moduleRow, 'rexmMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'rexmFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'rexmFSM', '', 1, '{:s}')
        self.position = ValueGB(self.moduleRow, 'rexm', 'Position', 0, '{:s}')

        self.switchA = ValueGB(self.moduleRow, 'rexmInfo', 'SwitchA', 0, '{:d}')
        self.switchB = ValueGB(self.moduleRow, 'rexmInfo', 'switchB', 1, '{:d}')
        self.speed = ValueGB(self.moduleRow, 'rexmInfo', 'Speed', 2, '{:d}')
        self.steps = ValueGB(self.moduleRow, 'rexmInfo', 'Steps', 3, '{:d}')

        self.commands = RexmCommands(self)

        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)
        self.grid.addWidget(self.position, 0, 3)

        self.grid.addWidget(self.switchA, 1, 0)
        self.grid.addWidget(self.switchB, 1, 1)
        self.grid.addWidget(self.speed, 1, 2)
        self.grid.addWidget(self.steps, 1, 3)

        self.grid.addWidget(self.empty, 2, 0, 3, 4)
        self.grid.addWidget(self.commands, 0, 4, 2.5, 3)
