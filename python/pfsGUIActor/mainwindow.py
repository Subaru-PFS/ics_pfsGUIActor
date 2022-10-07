__author__ = 'alefur'

from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QWidget, QMessageBox
from pfsGUIActor.common import GridLayout
from pfsGUIActor.module import SpsAitModule, SpecModule, PfiModule
from pfsGUIActor.tron.module import TronModule


class PfsWidget(QWidget):
    def __init__(self, pfsGUI):
        QWidget.__init__(self)
        self.pfsGUI = pfsGUI

        self.mainLayout = GridLayout()
        self.mainLayout.setSpacing(1)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        nCol = 4
        # add spacer
        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding), 1, nCol - 1)

        self.tronModule = TronModule(self)
        self.mainLayout.addWidget(self.tronModule, 1, nCol - 1, 1, 1)

        nRow = 2
        self.mainLayout.addWidget(SpsAitModule(self), nRow, 0, 1, nCol)

        for smId in range(1, 12):
            if 'sm%d' % smId not in self.actor.displayConfig.keys():
                continue

            nRow += 1
            specConfig = self.actor.displayConfig[f'sm{smId}']
            self.mainLayout.addWidget(SpecModule(self, smId=smId, specConfig=specConfig), nRow, 0, 1, nCol)

        if 'pfi' in self.actor.displayConfig.keys():
            self.mainLayout.addWidget(PfiModule(self), nRow + 1, 0, 1, nCol)

        self.setLayout(self.mainLayout)

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
