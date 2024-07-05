__author__ = 'alefur'

from functools import partial

import pfsGUIActor.styles as styles
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDialog, QGroupBox, QLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QWidget
from pfsGUIActor.common import PushButton, Icon, GridLayout, VBoxLayout, TabWidget
from pfsGUIActor.logs import CmdLogArea, RawLogArea
from pfsGUIActor.widgets import CmdButton


class ButtonBox(GridLayout):
    def __init__(self, controlDialog):
        GridLayout.__init__(self)
        self.controlDialog = controlDialog
        self.apply = PushButton('Apply')
        self.apply.clicked.connect(controlDialog.sendCommands)

        self.discard = PushButton('Discard')
        self.discard.clicked.connect(controlDialog.cancelCommands)

        self.showLogs = PushButton('Show Logs')
        self.hideLogs = PushButton('Hide Logs')
        self.showLogs.clicked.connect(partial(self.show, True))
        self.hideLogs.clicked.connect(partial(self.show, False))

        self.addWidget(self.showLogs, 0, 0)
        self.addWidget(self.hideLogs, 0, 0)
        self.addWidget(self.apply, 0, 9)
        self.addWidget(self.discard, 0, 10)

        self.show(False)

    def show(self, bool):
        self.showLogs.setVisible(not bool)
        self.hideLogs.setVisible(bool)
        self.controlDialog.logArea.setVisible(bool)
        self.controlDialog.adjustSize()


class Topbar(QHBoxLayout):
    def __init__(self, controlDialog):
        QHBoxLayout.__init__(self)
        self.setAlignment(Qt.AlignLeft)
        self.reload = CmdButton(controlPanel=None, label=' Reload Config ', controlDialog=controlDialog,
                                cmdStr='%s reloadConfiguration' % controlDialog.moduleRow.actorName)
        self.statusButton = CmdButton(controlPanel=None, label=' STATUS ', controlDialog=controlDialog,
                                      cmdStr='%s status' % controlDialog.moduleRow.actorName)
        self.addWidget(self.reload)
        self.addWidget(self.statusButton)

    def setEnabled(self, a0: bool):
        for item in [self.itemAt(i) for i in range(self.count())]:
            if issubclass(type(item), QLayout):
                item.setEnabled(a0)
            else:
                item.widget().setEnabled(a0)


class ControlDialog(QDialog):
    def __init__(self, moduleRow, title=False, addGridRows=False):
        self.moduleRow = moduleRow
        title = moduleRow.actorLabel if not title else title
        QDialog.__init__(self)
        self.cmdBuffer = dict()

        self.topbar = Topbar(self)
        self.tabWidget = TabWidget(self)

        self.logArea = TabWidget(self)

        self.cmdLog = CmdLogArea()
        self.rawLog = self.rawLogArea()
        self.logArea.addTab(self.cmdLog, 'cmdLog')
        self.logArea.addTab(self.rawLog, 'rawLog')

        self.buttonBox = ButtonBox(self)

        if not addGridRows:
            self.vbox = VBoxLayout()
            self.vbox.addLayout(self.topbar)
            self.vbox.addWidget(self.tabWidget)
            self.vbox.addLayout(self.buttonBox)
            self.vbox.addWidget(self.logArea)
            self.setLayout(self.vbox)
        else:
            self.grid = GridLayout()
            self.grid.setSizeConstraint(QLayout.SetMinimumSize)
            self.grid.addLayout(self.topbar, 0, 0, 1, 5)
            self.grid.addWidget(self.tabWidget, 1, 0, addGridRows, 9)
            self.grid.addLayout(self.buttonBox, addGridRows + 1, 0, 1, 9)
            self.grid.addWidget(self.logArea, addGridRows + 2, 0, 1, 9)
            self.setLayout(self.grid)

        self.setWindowTitle(title)
        self.setVisible(False)
        #self.move(self.moduleRow.mwindow.pfsGUI.screenWidth * 0.3, self.moduleRow.mwindow.pfsGUI.screenHeight * 0.5)

    def rawLogArea(self):
        return RawLogArea(self.moduleRow.actorName)

    @property
    def pannels(self):
        return [self.tabWidget.widget(i) for i in range(self.tabWidget.count())]

    def addCommand(self, button, cmdStr):
        self.cmdBuffer[button] = cmdStr

    def clearCommand(self, button):
        self.cmdBuffer.pop(button, None)

    def sendCommands(self):
        for button, fullCmd in self.cmdBuffer.items():
            [actor, cmdStr] = fullCmd.split(' ', 1)
            self.cmdLog.newLine('cmdIn=%s %s' % (actor, cmdStr))
            self.moduleRow.mwindow.sendCommand(actor=actor, cmdStr=cmdStr, callFunc=self.cmdLog.printResponse)
            button.setChecked(0)

        self.cmdBuffer.clear()

    def cancelCommands(self):
        for button, fullCmd in self.cmdBuffer.items():
            button.setChecked(0)

        self.cmdBuffer.clear()

    def close(self):
        self.hide()

    def setEnabled(self, a0: bool):
        for widget in [self.topbar] + self.pannels:
            widget.setEnabled(a0)


class ControlPanel(QWidget):
    def __init__(self, controlDialog, tabWidget=None):
        QWidget.__init__(self)
        self.controlDialog = controlDialog
        self.tabWidget = controlDialog.tabWidget if tabWidget is None else tabWidget

        self.grid = GridLayout()
        self.grid.setContentsMargins(*(4 * (1,)))
        self.grid.setSizeConstraint(QLayout.SetMinimumSize)
        self.setLayout(self.grid)

        self.createWidgets()
        self.setInLayout()
        self.setEnabled(False)

    @property
    def moduleRow(self):
        return self.controlDialog.moduleRow

    @property
    def actorName(self):
        return self.controlDialog.moduleRow.actorName

    def createWidgets(self):
        pass

    def setInLayout(self):
        pass

    def addCommandSet(self, commands):
        self.commands = commands
        self.grid.addWidget(self.commands, 0, self.grid.columnCount(), self.grid.rowCount(), self.grid.columnCount())
        self.spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.grid.addItem(self.spacer, self.grid.rowCount(), 0)

    def updateIcon(self, color):
        icon = Icon(f'{color}.png')
        self.tabWidget.setTabIcon(self.tabWidget.indexOf(self), icon)
        self.tabWidget.setIconSize(QSize(styles.bigFont + 2, styles.bigFont + 2))

    def updateStatusIcon(self, a0: bool):
        color = 'green' if a0 else 'gray'
        self.updateIcon(color)

    def setEnabled(self, a0: bool):
        self.updateStatusIcon(a0)

        for item in [self.grid.itemAt(i) for i in range(self.grid.count())]:
            if issubclass(type(item), QSpacerItem):
                continue
            elif issubclass(type(item), QLayout):
                item.setEnabled(a0)
            else:
                item.widget().setEnabled(a0)


class CommandsGB(QGroupBox):
    def __init__(self, controlPanel, fontSize=styles.smallFont):
        QGroupBox.__init__(self)
        self.controlPanel = controlPanel
        self.grid = GridLayout()
        self.grid.setContentsMargins(1, 7, 1, 1)
        self.setTitle('Commands')
        self.setLayout(self.grid)
        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 1ex;} " % (fontSize) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

    def setEnabled(self, a0: bool):
        for item in [self.grid.itemAt(i) for i in range(self.grid.count())]:
            if (issubclass(type(item), QSpacerItem)):
                continue
            elif (issubclass(type(item), QLayout)):
                item.setEnabled(a0)
            else:
                item.widget().setEnabled(a0)


class ControllerPanel(ControlPanel):
    def __init__(self, controlDialog, controllerName, tabWidget=None):
        self.controllerName = controllerName
        ControlPanel.__init__(self, controlDialog=controlDialog, tabWidget=tabWidget)

    def setEnabled(self, a0):
        a0 = self.controllerName in self.moduleRow.keyVarDict['controllers'] if a0 else False
        ControlPanel.setEnabled(self, a0)


class ControllerCmd(CommandsGB):
    def __init__(self, controlPanel, fontSize=styles.smallFont):
        CommandsGB.__init__(self, controlPanel=controlPanel, fontSize=fontSize)
        self.addButtons(controlPanel)

    def setEnabled(self, a0: bool):
        CommandsGB.setEnabled(self, a0)

        self.connectButton.setEnabled(self.controlPanel.moduleRow.isOnline)
        self.connectButton.setVisible(not a0)
        self.disconnectButton.setEnabled(self.controlPanel.moduleRow.isOnline)
        self.disconnectButton.setVisible(a0)

    def addButtons(self, controlPanel):
        actor, controller = controlPanel.actorName, controlPanel.controllerName
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s %s status' % (actor, controller))
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='%s connect controller=%s' % (actor, controller))
        self.disconnectButton = CmdButton(controlPanel=controlPanel, label='DISCONNECT',
                                          cmdStr='%s disconnect controller=%s' % (actor, controller))
        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)
        self.grid.addWidget(self.disconnectButton, 0, 1)


class MultiplePanel(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.grid = GridLayout()
        self.grid.setContentsMargins(*(4 * (1,)))
        self.setLayout(self.grid)

    def addWidget(self, *args, **kwargs):
        return self.grid.addWidget(*args, **kwargs)
