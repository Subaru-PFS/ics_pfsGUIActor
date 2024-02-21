__author__ = 'alefur'

from functools import partial

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QWidget, QMessageBox
from pfsGUIActor.ait.module import AitModule
from pfsGUIActor.common import GridLayout
from pfsGUIActor.module import SpecModule, SpsModule, PfiModule
from pfsGUIActor.tron.module import TronModule


class PfsWidget(QWidget):
    def __init__(self, pfsGUI):
        QWidget.__init__(self)
        self.isLocked = False
        self.pfsGUI = pfsGUI
        self.specModules = dict()

        self.mainLayout = GridLayout()
        self.setLayout(self.mainLayout)

        self.mainLayout.setSpacing(1)
        self.mainLayout.setContentsMargins(1, 1, 1, 1)

        self.aitModule = AitModule(self)
        self.tronModule = TronModule(self)
        self.spsModule = SpsModule(self)

        # building each specModule based on config.
        for specNum in range(1, 12):
            if 'sm%d' % specNum not in self.actor.displayConfig.keys():
                continue

            specConfig = self.actor.displayConfig[f'sm{specNum}']
            self.specModules[specNum] = SpecModule(self, specNum=specNum, specConfig=specConfig)

        # not the prettiest code you ever wrote but it works and is fairly clear.
        iRow = 0
        nCols = 4
        # add spacer
        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding), iRow, nCols - 1)
        self.mainLayout.addWidget(self.tronModule, iRow, nCols - 1, 1, 1)
        iRow += 1

        for module in [self.aitModule, self.spsModule] + list(self.specModules.values()):
            self.mainLayout.addWidget(module, iRow, 0, 1, nCols)
            iRow += 1

        if 'pfi' in self.actor.displayConfig.keys():
            self.mainLayout.addWidget(PfiModule(self), iRow + 1, 0, 1, nCols)
            iRow += 1

        self.spsModule.connect(self.specModules)
        self.adjustSize()

    @property
    def actor(self):
        return self.pfsGUI.actor

    @property
    def isConnected(self):
        return self.pfsGUI.isConnected

    def sendCommand(self, actor, cmdStr, callFunc):
        import opscore.actor.keyvar as keyvar
        self.actor.cmdr.bgCall(**dict(actor=actor,
                                      cmdStr=cmdStr,
                                      timeLim=1600,
                                      callFunc=callFunc,
                                      callCodes=keyvar.AllCodes))

    def adjustSize(self):
        if self.lock():
            return

        QTimer.singleShot(100, partial(QWidget.adjustSize, self))
        QTimer.singleShot(200, self.pfsGUI.adjustSize)
        QTimer.singleShot(500, self.unlock)

    def lock(self):
        wasLocked = self.isLocked
        self.isLocked = True if not wasLocked else wasLocked
        return wasLocked

    def unlock(self):
        self.isLocked = False

    def heartBeat(self):
        self.tronModule.tronStatus.dial.heartBeat()
        self.adjustSize()

    def showError(self, title, error):
        reply = QMessageBox.critical(self, title, error, QMessageBox.Ok)

    def setEnabled(self, a0: bool) -> None:
        widgets = [self.mainLayout.itemAt(i).widget() for i in range(self.mainLayout.count())]

        for widget in widgets:
            if widget is None:
                continue
            widget.setEnabled(a0)
