__author__ = 'alefur'

import pfsGUIActor.styles as styles
from PyQt5.QtWidgets import QGroupBox
from pfsGUIActor.cam import CamRow
from pfsGUIActor.common import GridLayout
from pfsGUIActor.enu import EnuRow
from pfsGUIActor.pfi.peb import PebRow
from pfsGUIActor.pfi.pfilamps import PfiLampsRow
from pfsGUIActor.sps import SpecModuleRow

# lam import


class Module(QGroupBox):
    def __init__(self, mwindow, title):
        QGroupBox.__init__(self)

        self.fontSize = int(round(1.25 * styles.bigFont))
        self.grid = GridLayout()
        self.grid.setContentsMargins(0, int(styles.bigFont * 0.8), 0, 0)
        self.grid.setSpacing(0)

        self.setLayout(self.grid)

        self.setTitle(title)
        self.mwindow = mwindow

        self.setStyleSheet()

    @property
    def rows(self):
        return []

    def populateLayout(self):
        for i, row in enumerate(self.rows):
            for j, widget in enumerate(row.displayed):
                if widget is None:
                    continue
                self.grid.addWidget(widget, i, j)

        self.adjustSize()

    def setEnabled(self, a0: bool) -> None:
        for row in self.rows:
            row.setOnline(a0)

        QGroupBox.setEnabled(self, a0)

    def showModule(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

        self.mwindow.adjustSize()

    def setStyleSheet(self, styleSheet=None):
        QGroupBox.setStyleSheet(self,
                                "QGroupBox{ font-size: %ipx ;font-weight: bold; " % self.fontSize +
                                "border: 1px solid lightgray;border-radius: 3px;margin-top: 6px;}")


class SpsModule(Module):
    def __init__(self, mwindow):
        Module.__init__(self, mwindow=mwindow, title='')

        self.row = SpecModuleRow(self)

        self.populateLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)

    @property
    def rows(self):
        return [self.row]

    def connect(self, specModules):
        """"""
        for specNum, specModule in specModules.items():
            for specLabel in self.row.specLabels:
                if specNum == specLabel.specNum:
                    specLabel.connect(specModule)


class SpecModule(Module):
    def __init__(self, mwindow, specNum, specConfig):
        self.specNum = specNum
        Module.__init__(self, mwindow=mwindow, title='Spectrograph Module %i' % specNum)

        parts = []

        for part in specConfig:
            if part == 'enu':
                parts.extend([EnuRow(self)])
            elif part in ['b', 'r', 'n']:
                parts.append(CamRow(self, arm=part))
            else:
                raise ValueError(f'unknown part:{part}')

        self.parts = parts

        self.populateLayout()

    @property
    def rows(self):
        return self.parts


class PfiModule(Module):
    def __init__(self, mwindow):
        Module.__init__(self, mwindow=mwindow, title='PFI')
        self.peb = PebRow(self)
        self.pfiLamps = PfiLampsRow(self)

        self.populateLayout()

    @property
    def rows(self):
        return [self.peb, self.pfiLamps]
