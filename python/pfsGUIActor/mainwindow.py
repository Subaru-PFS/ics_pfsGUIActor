__author__ = 'alefur'

from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QWidget, QMessageBox
from pfsGUIActor.common import GridLayout
from pfsGUIActor.module import AitModule, SpecModule, SpsModule, PfiModule
from pfsGUIActor.tron.module import TronModule


class PfsWidget(QWidget):
    def __init__(self, pfsGUI):
        QWidget.__init__(self)
        self.pfsGUI = pfsGUI
        self.specModules = dict()

        self.mainLayout = GridLayout()
        self.setLayout(self.mainLayout)

        self.mainLayout.setSpacing(5)
        self.mainLayout.setContentsMargins(1, 1, 1, 1)

        nCol = 4
        # add spacer
        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding), 1, nCol - 1)

        self.tronModule = TronModule(self)
        self.mainLayout.addWidget(self.tronModule, 1, nCol - 1, 1, 1)

        nRow = 2
        self.mainLayout.addWidget(AitModule(self), nRow, 0, 1, nCol)
        nRow += 1
        self.spsModule = SpsModule(self)
        self.mainLayout.addWidget(self.spsModule, nRow, 0, 1, nCol)

        for specNum in range(1, 12):
            if 'sm%d' % specNum not in self.actor.displayConfig.keys():
                continue

            nRow += 1

            specConfig = self.actor.displayConfig[f'sm{specNum}']
            self.specModules[specNum] = SpecModule(self, specNum=specNum, specConfig=specConfig)
            self.mainLayout.addWidget(self.specModules[specNum], nRow, 0, 1, nCol)

        if 'pfi' in self.actor.displayConfig.keys():
            self.mainLayout.addWidget(PfiModule(self), nRow + 1, 0, 1, nCol)

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
        QWidget.adjustSize(self)
        self.pfsGUI.adjustSize()

    def heartBeat(self):
        self.tronModule.tronStatus.dial.heartBeat()

    def showError(self, title, error):
        reply = QMessageBox.critical(self, title, error, QMessageBox.Ok)

    def setEnabled(self, a0: bool) -> None:
        widgets = [self.mainLayout.itemAt(i).widget() for i in range(self.mainLayout.count())]

        for widget in widgets:
            if widget is None:
                continue
            widget.setEnabled(a0)
