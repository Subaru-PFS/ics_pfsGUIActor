__author__ = 'alefur'
from PyQt5.QtWidgets import QGridLayout, QComboBox

from spsClient.widgets import Coordinates, ValueGB, ControlPanel, CommandsGB, CmdButton, DoubleSpinBoxGB, CustomedCmd


class CoordBoxes(QGridLayout):
    def __init__(self):
        QGridLayout.__init__(self)
        self.widgets = [DoubleSpinBoxGB('X', -10, 10, 5),
                        DoubleSpinBoxGB('Y', -10, 10, 5),
                        DoubleSpinBoxGB('Z', -10, 10, 5),
                        DoubleSpinBoxGB('U', -2, 2, 5),
                        DoubleSpinBoxGB('V', -2, 2, 5),
                        DoubleSpinBoxGB('W', -2, 2, 5)]

        for i, spinbox in enumerate(self.widgets):
            self.addWidget(spinbox, i // 3, i % 3)


class MoveCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='MOVE')

        self.combo = QComboBox()
        self.combo.addItems(['absolute', 'relative'])
        self.combo.currentIndexChanged.connect(self.resetCoords)

        self.addWidget(self.combo, 0, 1)

    @property
    def spinboxes(self):
        return self.controlPanel.commands.coordBoxes.widgets

    def resetCoords(self, ind):
        if ind == 0:
            vals = [float(valueGB.value.text()) for valueGB in self.controlPanel.coordinates.widgets]
        else:
            vals = 6 * [0]

        for spinbox, val in zip(self.spinboxes, vals):
            spinbox.setValue(val)

    def buildCmd(self):
        labels = ['X', 'Y', 'Z', 'U', 'V', 'W']
        values = [spinbox.getValue() for spinbox in self.spinboxes]

        cmdStr = '%s slit move %s ' % (self.controlPanel.enuActor, self.combo.currentText())
        cmdStr += (" ".join(['%s=%.5f' % (label, value) for label, value in zip(labels, values)]))

        return cmdStr


class SetRepCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SET')

        self.combo = QComboBox()
        self.combo.addItems(['home', 'tool'])
        self.combo.currentIndexChanged.connect(self.resetCoords)

        self.addWidget(self.combo, 0, 1)

    def resetCoords(self, ind):
        for spinbox in self.spinboxes:
            spinbox.setValue(0)

    @property
    def spinboxes(self):
        return self.controlPanel.commands.coordBoxes.widgets

    def buildCmd(self):
        labels = ['X', 'Y', 'Z', 'U', 'V', 'W']
        values = [spinbox.getValue() for spinbox in self.spinboxes]

        cmdStr = '%s slit set %s ' % (self.controlPanel.enuActor, self.combo.currentText().lower())
        cmdStr += (" ".join(['%s=%.5f' % (label, value) for label, value in zip(labels, values)]))

        return cmdStr


class SlitCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)

        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='%s connect controller=slit' % controlPanel.enuActor)
        self.initButton = CmdButton(controlPanel=controlPanel, label='INIT',
                                    cmdStr='%s slit init' % controlPanel.enuActor)
        self.abortButton = CmdButton(controlPanel=controlPanel, label='ABORT',
                                     cmdStr='%s slit abort' % controlPanel.enuActor)
        self.goHomeButton = CmdButton(controlPanel=controlPanel, label='GO HOME',
                                      cmdStr='%s slit move home' % controlPanel.enuActor)
        self.coordBoxes = CoordBoxes()

        self.moveCmd = MoveCmd(controlPanel=controlPanel)
        self.setRepCmd = SetRepCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.connectButton, 0, 0)
        self.grid.addWidget(self.initButton, 0, 1)
        self.grid.addWidget(self.abortButton, 0, 2)
        self.grid.addLayout(self.coordBoxes, 1, 0, 2, 3)
        self.grid.addLayout(self.moveCmd, 3, 0, 1, 2)
        self.grid.addLayout(self.setRepCmd, 4, 0, 1, 2)
        self.grid.addWidget(self.goHomeButton, 5, 0, 1, 1)

    @property
    def buttons(self):
        return [self.connectButton, self.initButton, self.abortButton,
                self.goHomeButton, self.moveCmd.button, self.setRepCmd.button]


class SlitPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.mode = ValueGB(self.moduleRow, 'slitMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'slitFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'slitFSM', '', 1, '{:s}')
        self.info = ValueGB(self.moduleRow, 'slitInfo', 'Info', 0, '{:s}')
        self.location = ValueGB(self.moduleRow, 'slitLocation', 'Location', 0, '{:s}')

        self.coordinates = Coordinates(self.moduleRow, 'slit', title='Position')
        self.home = Coordinates(self.moduleRow, 'slitHome', title='Home')
        self.tool = Coordinates(self.moduleRow, 'slitTool', title='Tool')

        self.commands = SlitCommands(self)

        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)
        self.grid.addWidget(self.location, 0, 3)

        self.grid.addWidget(self.info, 1, 0, 1, 6)
        self.grid.addWidget(self.coordinates, 2, 0, 1, 6)
        self.grid.addWidget(self.home, 3, 0, 1, 6)
        self.grid.addWidget(self.tool, 4, 0, 1, 6)

        self.grid.addWidget(self.commands, 0, 7, 5, 4)

    @property
    def enuActor(self):
        return self.controlDialog.moduleRow.actorName

    @property
    def customWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())] + self.coordinates.widgets + \
               self.home.widgets + self.tool.widgets + self.commands.buttons
