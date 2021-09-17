__author__ = 'alefur'

import pfsGUIActor.dcb as dcb
import pfsGUIActor.lam as lamAIT
import pfsGUIActor.styles as styles
from PyQt5.QtWidgets import QGroupBox
from pfsGUIActor.cam import CamRow
from pfsGUIActor.common import GridLayout
from pfsGUIActor.enu import EnuRow
from pfsGUIActor.rough import RoughRow
from pfsGUIActor.sps import SpecModuleRow
from pfsGUIActor.pfi.peb import PebRow
from pfsGUIActor.pfi.pfilamps import PfiLampsRow

class Module(QGroupBox):
    def __init__(self, mwindow, title):
        QGroupBox.__init__(self)
        self.grid = GridLayout()
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
        styleSheet = "QGroupBox {font-size: %ipt;border: 1px solid lightgray;border-radius: 3px;margin-top: 6px;} " % round(
            0.9 * styles.bigFont) \
                     + "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top left; padding: 0 0px;}"
        QGroupBox.setStyleSheet(self, styleSheet)


class SpsAitModule(Module):
    def __init__(self, mwindow):
        Module.__init__(self, mwindow=mwindow, title='AIT')
        actors = [actor.strip() for actor in mwindow.actor.config.get('ait', 'actors').split(',')]

        self.dcbs = []

        if 'dcb' in actors:
            self.dcbs += dcb.DcbRow(self).rows
        if 'dcb2' in actors:
            self.dcbs += dcb.DcbRow(self, 'dcb2').rows

        lamAITRows = [lamAIT.aten.AtenRow(self).rows] if 'aten' in actors else []
        lamAITRows += [lamAIT.sac.SacRow(self)] if 'sac' in actors else []
        lamAITRows += [lamAIT.breva.BrevaRow(self)] if 'breva' in actors else []

        self.lamAITRows = lamAITRows

        roughs = ['rough1'] if 'rough1' in actors else []
        roughs += (['rough2'] if 'rough2' in actors else [])

        self.roughs = [RoughRow(self, rough) for rough in roughs]

        self.populateLayout()
        self.adjustSize()

    @property
    def rows(self):
        return self.dcbs + self.roughs + self.lamAITRows


class SpecModule(Module):
    def __init__(self, mwindow, smId, enu=True, arms=None):
        Module.__init__(self, mwindow=mwindow, title='Spectrograph Module %i' % smId)
        arms = ['b', 'r', 'n'] if arms is None else arms

        self.smId = smId
        self.spec = [SpecModuleRow(self, smId), EnuRow(self)] if enu else []
        self.cams = [CamRow(self, arm=arm) for arm in arms]

        self.populateLayout()
        self.adjustSize()

    @property
    def rows(self):
        return self.spec + self.cams


class PfiModule(Module):
    def __init__(self, mwindow):
        Module.__init__(self, mwindow=mwindow, title='PFI')
        self.peb = PebRow(self)
        self.pfiLamps = PfiLampsRow(self)

        self.populateLayout()
        self.adjustSize()

    @property
    def rows(self):
        return [self.peb]
