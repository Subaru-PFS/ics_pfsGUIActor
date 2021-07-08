__author__ = 'alefur'

import spsGUIActor.dcb as dcb
import spsGUIActor.styles as styles
from PyQt5.QtWidgets import QGroupBox
from spsGUIActor.aten import AtenRow
from spsGUIActor.breva import BrevaRow
from spsGUIActor.cam import CamRow
from spsGUIActor.common import GridLayout
from spsGUIActor.enu import EnuRow
from spsGUIActor.rough import RoughRow
from spsGUIActor.sac import SacRow
from spsGUIActor.sps import SpsRow


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


class AitModule(Module):
    def __init__(self, mwindow, aitActors):
        Module.__init__(self, mwindow=mwindow, title='AIT')

        self.aten = AtenRow(self).rows if 'aten' in aitActors else []
        self.sac = [SacRow(self)] if 'sac' in aitActors else []
        self.breva = [BrevaRow(self)] if 'breva' in aitActors else []

        self.populateLayout()
        self.adjustSize()

    @property
    def rows(self):
        return self.aten + self.sac + self.breva


class SpecModule(Module):
    def __init__(self, mwindow, smId, enu=True, arms=None):
        Module.__init__(self, mwindow=mwindow, title='Spectrograph Module %i' % smId)
        arms = ['b', 'r', 'n'] if arms is None else arms

        self.smId = smId
        self.enu = [EnuRow(self)] if enu else []
        self.cams = [CamRow(self, arm=arm) for arm in arms]

        self.populateLayout()
        self.adjustSize()

    @property
    def rows(self):
        return self.enu + self.cams


class SpsModule(Module):
    def __init__(self, mwindow, spsActors):
        Module.__init__(self, mwindow=mwindow, title='Spectrograph System')

        self.dcbs = []

        if 'dcb' in spsActors:
            self.dcbs += dcb.DcbRow(self).rows
        if 'dcb2' in spsActors:
            self.dcbs += dcb.DcbRow(self, 'dcb2').rows

        roughs = ['rough1'] if 'rough1' in spsActors else []
        roughs += (['rough2'] if 'rough2' in spsActors else [])

        self.roughs = [RoughRow(self, rough) for rough in roughs]
        self.sps = SpsRow(self)

        self.populateLayout()
        self.adjustSize()


    @property
    def rows(self):
        return self.dcbs + self.roughs + [self.sps]
