__author__ = 'alefur'

import pfsGUIActor.dcb as dcb
import pfsGUIActor.lam.aten as lamAten
import pfsGUIActor.lam.breva as lamBreva
import pfsGUIActor.lam.sac as lamSac
import pfsGUIActor.styles as styles
from PyQt5.QtWidgets import QGroupBox
from pfsGUIActor.cam import CamRow
from pfsGUIActor.common import GridLayout
from pfsGUIActor.enu import EnuRow
from pfsGUIActor.pfi.peb import PebRow
from pfsGUIActor.pfi.pfilamps import PfiLampsRow
from pfsGUIActor.rough import RoughRow
from pfsGUIActor.sps import SpecModuleRow

# lam import
import pfsGUIActor.lam.aten as lamAten
import pfsGUIActor.lam.sac as lamSac
import pfsGUIActor.lam.breva as lamBreva


class Module(QGroupBox):
    def __init__(self, mwindow, title):
        QGroupBox.__init__(self)

        self.grid = GridLayout()
        self.grid.setContentsMargins(0, 7, 0, 0)
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

    def setEnabled(self, a0: bool) -> None:
        for row in self.rows:
            row.setOnline(a0)

        QGroupBox.setEnabled(self, a0)

    def setStyleSheet(self, styleSheet=None):
        QGroupBox.setStyleSheet(self,
                                "QGroupBox{ font-size: %ipx ;font-weight: bold; " % (round(1.25 * styles.bigFont)) +
                                "border: 1px solid lightgray;border-radius: 3px;margin-top: 6px;}")


class AitModule(Module):
    def __init__(self, mwindow):
        Module.__init__(self, mwindow=mwindow, title='AIT')
        actors = mwindow.actor.displayConfig['ait']

        self.dcbs = []

        if 'dcb' in actors:
            self.dcbs += dcb.DcbRow(self).rows
        if 'dcb2' in actors:
            self.dcbs += dcb.DcbRow(self, 'dcb2').rows

        lamAITRows = []
        lamAITRows += lamAten.AtenRow(self).rows if 'aten' in actors else []
        lamAITRows += [lamSac.SacRow(self)] if 'sac' in actors else []
        lamAITRows += [lamBreva.BrevaRow(self)] if 'breva' in actors else []

        self.lamAITRows = lamAITRows

        roughs = ['rough1'] if 'rough1' in actors else []
        roughs += (['rough2'] if 'rough2' in actors else [])

        self.roughs = [RoughRow(self, rough) for rough in roughs]

        self.populateLayout()
        self.adjustSize()

    @property
    def rows(self):
        return self.dcbs + self.roughs + self.lamAITRows


class SpsModule(Module):
    def __init__(self, mwindow):
        Module.__init__(self, mwindow=mwindow, title='')

        self.row = SpecModuleRow(self)

        self.populateLayout()
        self.adjustSize()

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
        self.adjustSize()

    @property
    def rows(self):
        return self.parts


class PfiModule(Module):
    def __init__(self, mwindow):
        Module.__init__(self, mwindow=mwindow, title='PFI')
        self.peb = PebRow(self)
        self.pfiLamps = PfiLampsRow(self)

        self.populateLayout()
        self.adjustSize()

    @property
    def rows(self):
        return [self.peb, self.pfiLamps]
