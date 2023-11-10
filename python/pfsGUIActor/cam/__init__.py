__author__ = 'alefur'

import os

import pfsGUIActor.styles as styles
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QDialog, QGroupBox, QGridLayout, QLayout
from pfsGUIActor.common import PushButton, imgPath, GridLayout, TabWidget, Label
from pfsGUIActor.control import ControlDialog, ButtonBox, ControlPanel, ControllerPanel
from pfsGUIActor.logs import CmdLogArea
from pfsGUIActor.modulerow import ActorGB, ModuleRow
from pfsGUIActor.widgets import ValueGB


class CamLabel(Label):
    def __init__(self, label):
        super().__init__(label.upper())

        # Set font properties
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.setFont(font)

        # Set background to transparent
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(0, 0, 0, 0))
        self.setPalette(palette)

        # Set text color to white
        self.setStyleSheet("color: white;")


class CamDevice(QGroupBox):
    def __init__(self, controlDialog, controllerName, title=None):
        title = controllerName.capitalize() if title is None else title
        self.controllerName = controllerName

        QGroupBox.__init__(self)
        self.controlDialog = controlDialog
        self.grid = GridLayout()
        self.grid.setSizeConstraint(QLayout.SetMinimumSize)
        self.grid.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.grid)

        self.createWidgets()
        self.setInLayout()

        self.setTitle(title)
        self.setCheckable(True)
        self.setEnabled(False)

    @property
    def moduleRow(self):
        return self.controlDialog.moduleRow

    @property
    def actorName(self):
        return self.controlDialog.moduleRow.actorName

    def addCommandSet(self, commands):
        ControlPanel.addCommandSet(self, commands)

    def updateStatusIcon(self, a0):
        filename = 'green.png' if a0 else 'gray.png'
        self.setStyleSheet(
            "CamDevice {font-size: %dpt; font-weight:bold;border: 1px solid #000000;border-radius: 20;;margin-top: 10px;}"
            "CamDevice::title {subcontrol-origin: margin;subcontrol-position: top left; padding: 0 10px;}"
            "CamDevice::indicator { width:%ipx; height: %ipx;}"
            "CamDevice::indicator:checked {image: url(%s);} " % (
                styles.smallFont, styles.bigFont + 2, styles.bigFont + 2, os.path.join(imgPath, filename)))

    def setEnabled(self, a0):
        ControllerPanel.setEnabled(self, a0)


class ExposureState(ValueGB):
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        ValueGB.__init__(self, moduleRow, 'exposureState', '', 0, '{:s}')

    def setText(self, txt):
        txt = txt.upper()
        ValueGB.setText(self, txt)


from pfsGUIActor.cam.ccd import CcdRow
from pfsGUIActor.cam.hx import HxRow
from pfsGUIActor.cam.xcu import XcuRow


class CamStatus(ActorGB, QGroupBox):
    def __init__(self, cam):
        self.cam = cam
        self.fontSize = styles.bigFont
        QGroupBox.__init__(self)
        self.setTitle('Actor')

        self.button = PushButton()
        self.button.setFlat(True)

        self.grid = QGridLayout()
        self.grid.addWidget(self.button, 0, 0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)

        self.setColor(*styles.colorWidget('offline'))
        self.setText(cam.label)

    def setStatus(self, status):
        if status == 0:
            self.setColor(*styles.colorWidget('offline'))
        if status == 1:
            self.setColor(*styles.colorWidget('midstate'))
        if status == 2:
            self.setColor(*styles.colorWidget('online'))


class CamRow(ModuleRow):
    def __init__(self, module, arm):
        self.module = module
        self.arm = arm
        self.label = '%sCU' % arm.upper()
        self.actorStatus = CamStatus(self)
        self.actorStatus.button.clicked.connect(self.showDetails)

        DetectorRow = CcdRow if arm in ['b', 'r'] else HxRow
        self.detector = DetectorRow(self)
        self.xcu = XcuRow(self)

        self.createDialog(CamDialog(self))

    @property
    def displayed(self):
        return [self.actorStatus, self.xcu.cryoMode, self.detector.substate, self.xcu.temperature, self.xcu.pressure,
                self.xcu.twoIonPumps]

    @property
    def isNir(self):
        return self.arm == 'n'

    def setOnline(self, isOnline=None):
        status = sum([self.detector.isOnline + self.xcu.isOnline]) if isOnline is None else int(isOnline)
        self.actorStatus.setStatus(status)


class CamDialog(ControlDialog):
    back = dict(b=['3a74bc', '0f2949'], r=['bd3946', '4a0f15'], n=['434343', '000000'])

    def __init__(self, camRow):
        self.moduleRow = camRow
        light, dark = CamDialog.back[camRow.arm]
        QDialog.__init__(self)
        self.setWindowTitle('%s %i' % (camRow.label, camRow.module.specNum))

        self.setStyleSheet(
            "QDialog { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0.25,stop: 0 #%s, stop: 1 #%s);}" % (
                light, dark))

        self.grid = GridLayout()
        self.grid.setSizeConstraint(QLayout.SetMinimumSize)
        self.tabWidget = TabWidget(self)
        self.cmdBuffer = dict()

        self.moduleRow.xcu.createDialog(self.tabWidget)
        self.moduleRow.detector.createDialog(self.tabWidget)

        self.logArea = TabWidget(self)
        self.cmdLog = CmdLogArea()
        self.logArea.addTab(self.cmdLog, 'cmdLog')
        self.logArea.addTab(self.xcuDialog.rawLogArea(), 'xcuLog')
        self.logArea.addTab(self.detectorDialog.rawLogArea(), 'detectorLog')

        buttonBox = ButtonBox(self)

        self.grid.addLayout(self.xcuDialog.topbar, 0, 0, 1, 5)
        self.grid.addLayout(self.detectorDialog.topbar, 1, 0, 1, 3)
        self.grid.addWidget(CamLabel(f'{camRow.label[0]}{camRow.module.specNum}'), 0, 8, 2, 1)
        self.grid.addWidget(self.tabWidget, 2, 0, 1, 9)
        self.grid.addLayout(buttonBox, 3, 0, 1, 9)
        self.grid.addWidget(self.logArea, 4, 0, 1, 9)

        self.setLayout(self.grid)
        self.setVisible(False)

    @property
    def detectorDialog(self):
        return self.moduleRow.detector.controlDialog

    @property
    def xcuDialog(self):
        return self.moduleRow.xcu.controlDialog
