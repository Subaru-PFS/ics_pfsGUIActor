__author__ = 'alefur'

import re
from datetime import datetime as dt
from functools import partial

import ics.utils.instdata.io as instdataIO
import pfsGUIActor.styles as styles
import pfsGUIActor.tron.obsWarnings.warningFactory as warningFactory
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import QPlainTextEdit, QMenu
from pfsGUIActor.control import ControlDialog, ControlPanel
from pfsGUIActor.logs import CmdLogArea
from pfsGUIActor.modulerow import ModuleRow
from pfsGUIActor.widgets import ValueMRow
from pfsGUIActor.widgets import ValuesRow, ValueGB


class Model:
    """Manages control panel and actor interaction, adds warnings and checks actor online status."""

    def __init__(self, controlPanel, actorName):
        self.controlPanel = controlPanel
        self.actorName = actorName

    @property
    def hubModuleRow(self):
        return self.controlPanel.moduleRow

    @property
    def keyVarDict(self):
        return self.hubModuleRow.models[self.actorName].keyVarDict

    @property
    def mwindow(self):
        return self.hubModuleRow.mwindow

    @property
    def isOnline(self):
        return self.actorName in self.hubModuleRow.keyVarDict['actors']

    def addWarning(self, keyDescription, keyConfig):
        """Add a warning key based on description and config."""
        self.key = WarningKey(self, keyDescription, keyConfig)
        return self.key

    def warn(self, message):
        """Send a warning message based on current status."""
        currentStatus = [widget.value.text() for widget in self.key.widgets]
        self.controlPanel.warningBuffer.scream(f'{self.key.keyName}={",".join(currentStatus)}', message)


class WarningVal(ValueGB):
    """
    Represents a warning value with logic to check and alert for warnings.
    """

    def __init__(self, *args, warningLogic=None, **kwargs):
        self.warningLogic = warningLogic
        super().__init__(*args, **kwargs)

    def setText(self, txt):
        super().setText(txt)
        status = self.warningLogic.check(txt)
        if status != 'OK':
            self.moduleRow.warn(status)


class WarningKey(ValuesRow):
    """Creates widgets to display and control warnings based on model and config."""
    translate = {int: '{:g}', float: '{:g}', str: '{:s}'}

    def __init__(self, model, keyDescription, keyConfig):
        self.model = model
        self.widgets = []
        self.keyName = self.createWidgets(keyDescription, keyConfig)
        super().__init__(self.widgets, title='')

    def getKeyNameAndIdentifier(self, keyDescription):
        """Extract key name and identifier from description."""
        pattern = r"(\w+)\[(\w+|\d+)\]"
        match = re.search(pattern, keyDescription)
        return match.groups() if match else (keyDescription, '0')

    def createWidgets(self, keyDescription, keyConfig):
        """Create widgets based on description and config."""
        keyName, identifier = self.getKeyNameAndIdentifier(keyDescription)
        keyVar = self.model.keyVarDict[keyName]
        infos = [(vtype.name, vtype.baseType) for vtype in keyVar.key.typedValues.vtypes]

        try:
            index = int(identifier)
        except ValueError:
            index = [inf[0] for inf in infos].index(identifier)

        for i, (name, type) in enumerate(infos):
            if i == index:
                widget = WarningVal(self.model, keyVar.name, name, i, WarningKey.translate[type],
                                    warningLogic=warningFactory.build(keyDescription, **keyConfig))
            else:
                widget = ValueGB(self.model, keyVar.name, name, i, WarningKey.translate[type])

            self.widgets.append(widget)

        return keyName


class Status(ValueMRow):
    """Status row to display warning state as 'OK' or 'WARNING'."""

    def __init__(self, moduleRow):
        super().__init__(moduleRow, 'actors', 'WARNINGS', 0, '{:s}')
        self.warningStatus = 'OK'

    def setText(self, *args, **kwargs):
        """Update displayed text based on warning status."""
        super().setText(self.warningStatus)

    def setStatus(self, anyWarning):
        """Set status based on presence of warnings."""
        self.warningStatus = 'WARNING' if anyWarning else 'OK'
        self.setText()


class WarningsRow(ModuleRow):
    """Row to manage and display warnings status for modules."""

    def __init__(self, module):
        super().__init__(module=module, actorName='hub', actorLabel='')
        self.status = Status(self)
        self.status.grid.addWidget(self.actorStatus.button, 0, 0)
        self.createDialog(WarningsDialog(self))

    @property
    def widgets(self):
        return [self.status]

    def updateStatus(self):
        """Check and update warning status for all panels."""
        anyWarning = any(p.warningBuffer.any() for p in self.controlDialog.pannels)
        self.status.setStatus(anyWarning)


class WarningBuffer(QPlainTextEdit):
    """Buffer to display, manage, and clear warnings."""

    def __init__(self, controlPanel):
        super().__init__()
        self.controlPanel = controlPanel
        self.warnings = []  # Stores warning lines

        # UI setup
        self.setMinimumSize(720, 180)
        self.setMaximumBlockCount(10000)
        self.setReadOnly(True)
        self.setStyleSheet("background-color: black; color: white;")
        self.setFont(QFont("Monospace", styles.smallFont))

    def newLine(self, status, message):
        """Add a warning with timestamp and formatted color."""
        timestamp = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"{timestamp} {status} {message}"
        self.warnings.append(line)

        color, _ = styles.colorWidget(CmdLogArea.colorCode['i'])
        self.appendHtml(f'\n<font color="{color}">{line}</font>')
        self.ensureCursorVisible()

    def contextMenuEvent(self, event):
        """Create context menu for clearing lines with highlighting."""
        cursor = self.cursorForPosition(event.pos())
        cursor.select(QTextCursor.LineUnderCursor)
        self.setTextCursor(cursor)  # Highlight selected line

        selectedLine = cursor.selectedText()
        if selectedLine:
            menu = QMenu(self)
            clearAction = menu.addAction("Clear")
            clearAllAction = menu.addAction("Clear All")
            action = menu.exec_(self.mapToGlobal(event.pos()))

            self.moveCursor(QTextCursor.End)  # Remove highlight after menu

            if action == clearAction:
                self.doClear(selectedLine)
            elif action == clearAllAction:
                self.doClear(singleLine=False)

    def doClear(self, singleLine=False):
        """Remove specific or all warning lines."""
        if not singleLine:
            self.warnings = []
        else:
            cleanedLine = singleLine.strip()
            self.warnings = [w for w in self.warnings if w != cleanedLine]
        self.refreshWarnings()

    def refreshWarnings(self):
        """Redraw all warnings from internal list."""
        self.clear()
        for warning in self.warnings:
            self.appendHtml(f'<font color="white">{warning}</font>')
        self.controlPanel.updateStatusIcon(True)

    def scream(self, status, message):
        """Add a new warning if control panel is online."""
        if self.controlPanel.isOnline:
            self.newLine(status, message)
            self.controlPanel.updateStatusIcon(True)

    def any(self):
        """Check if any warnings exist."""
        return bool(self.warnings)


class WarningPanel(ControlPanel):
    """Panel to display warnings and manage widgets for warning settings."""

    def __init__(self, controlDialog, tabWidget, actorName, config):
        self.model = Model(self, actorName)
        self.config = config
        self.warningBuffer = WarningBuffer(self)
        super().__init__(controlDialog=controlDialog, tabWidget=tabWidget)

    @property
    def isOnline(self):
        return self.model.actorName in self.moduleRow.keyVarDict['actors']

    def createWidgets(self):
        """Initialize widgets based on configuration."""
        for iRow, keyConfig in enumerate(self.config.items()):
            row = self.model.addWarning(*keyConfig)
            self.grid.addWidget(row, iRow, 0)

        self.grid.addWidget(self.warningBuffer, iRow + 1, 0)

    def setInLayout(self):
        """Placeholder for layout spacer setup."""
        pass

    def setEnabled(self, enabled):
        """Enable or disable the panel based on actor online status."""
        enabled = self.isOnline if enabled else False
        super().setEnabled(enabled)

    def updateStatusIcon(self, hasWarning):
        """Update icon based on warning status."""
        if not hasWarning:
            return self.updateIcon('gray')

        iconColor = 'red' if self.warningBuffer.any() else 'green'
        self.updateIcon(iconColor)
        self.controlDialog.moduleRow.updateStatus()

    def widgetList(self):
        """Return list of all non-empty widgets."""
        return [self.layout().itemAt(j).widget() for j in range(self.layout().count()) if
                self.layout().itemAt(j).widget()]

    def hideAll(self):
        """Hide all widgets in the panel."""
        for widget in self.widgetList():
            widget.hide()
        self.adjustSize()

    def showAll(self):
        """Show all widgets in the panel."""
        for widget in self.widgetList():
            widget.show()
        self.adjustSize()


class WarningsDialog(ControlDialog):
    """Dialog to manage and display warnings from multiple actors."""

    def __init__(self, warningsRow):
        super().__init__(moduleRow=warningsRow, title='WARNINGS')
        self.isLocked = False

        warningsConfig = self.loadWarningsConfig()
        for actor, warningConfig in warningsConfig.items():
            self.addWarningPanel(self.tabWidget, actor, warningConfig=warningConfig)

        # Connect tab changes to window resizing for better UX
        self.tabWidget.currentChanged.connect(partial(self.adjustWindowSize, self.tabWidget))
        self.tabWidget.tabBarClicked.connect(partial(self.adjustWindowSize, self.tabWidget))
        self.tabWidget.setUsesScrollButtons(False)

        self.adjustWindowSize(self.tabWidget, index=0)

    def addWarningPanel(self, tabWidget, actorName, warningConfig=None, title=None):
        """Add a warning panel for a specified actor with optional configuration."""
        title = title or actorName
        warningPanel = WarningPanel(self, tabWidget, actorName, warningConfig)
        warningPanel.hideAll()
        tabWidget.addTab(warningPanel, title)

    @property
    def pannels(self):
        """Return all warning panels in the tab widget."""
        return [self.tabWidget.widget(i) for i in range(self.tabWidget.count())]

    @property
    def site(self):
        """Return the site associated with the current module row."""
        return self.moduleRow.module.mwindow.actor.site

    def loadWarningsConfig(self):
        """Load the warnings configuration from instdata."""
        return instdataIO.loadConfig('obsWarnings', subDirectory='alerts')['actors']

    def adjustWindowSize(self, tabWidget, index):
        """Adjust the dialog window size when changing tabs."""
        if self.lock():
            return

        widget = tabWidget.widget(index)
        for panel in self.pannels:
            panel.hideAll()

        widget.showAll()
        QTimer.singleShot(10, self.adjustSize)
        QTimer.singleShot(100, self.unlock)

    def lock(self):
        """Lock the window size adjustments temporarily."""
        wasLocked = self.isLocked
        self.isLocked = True if not wasLocked else wasLocked
        return wasLocked

    def unlock(self):
        """Unlock the window size adjustments."""
        self.isLocked = False
