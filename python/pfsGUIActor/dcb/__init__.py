__author__ = 'alefur'

from pfsGUIActor.control import ControlDialog
from pfsGUIActor.dcb.collimator import CollimatorPanel
from pfsGUIActor.dcb.filterwheel import FilterwheelPanel
from pfsGUIActor.dcb.lamps import LampsPanel
from pfsGUIActor.enu import ConnectCmd
from pfsGUIActor.modulerow import ModuleRow, RowWidget
from pfsGUIActor.widgets import ValueMRow, SwitchMRow, Controllers


class DesignId(ValueMRow):
    def __init__(self, controlDialog):
        ValueMRow.__init__(self, controlDialog.moduleRow, 'designId', 'pfsDesignId', 0, '0x{:016x}')

    def updateVals(self, ind, fmt, keyvar):
        try:
            values = keyvar.getValue()
            values = (values,) if not isinstance(values, tuple) else values
            value = values[ind]
            strValue = fmt.format(value)

        except (ValueError, TypeError):
            strValue = 'UNDEFINED'

        self.setText(strValue)
        self.moduleRow.mwindow.heartBeat()


class RowOne(RowWidget):
    def __init__(self, dcbRow):
        RowWidget.__init__(self, dcbRow)

    @property
    def widgets(self):
        dcbRow = self.moduleRow
        states = [dcbRow.state, dcbRow.substate]
        return states + [dcbRow.powerFilterwheel, dcbRow.linewheel, dcbRow.qthwheel, dcbRow.adc1]


class RowTwo(RowWidget):
    def __init__(self, dcbRow):
        RowWidget.__init__(self, dcbRow)

    @property
    def widgets(self):
        dcbRow = self.moduleRow

        if dcbRow.actorName == 'dcb':
            lamps = [dcbRow.qth, dcbRow.neon, dcbRow.hgar, dcbRow.argon, dcbRow.krypton, dcbRow.allFiberLamp]
        else:
            lamps = [dcbRow.qth, dcbRow.neon, dcbRow.hgar, dcbRow.argon, dcbRow.krypton, dcbRow.xenon]

        return lamps

    @property
    def displayed(self):
        return [None, ] + self.widgets


class DcbRow(ModuleRow):
    def __init__(self, spsModule, name='dcb'):
        ModuleRow.__init__(self, module=spsModule, actorName=name, actorLabel=name.upper())

        self.state = ValueMRow(self, 'metaFSM', '', 0, '{:s}')
        self.substate = ValueMRow(self, 'metaFSM', '', 1, '{:s}')

        self.hgar = SwitchMRow(self, 'hgar', 'Hg-Ar', 0, '{:g}', controllerName='lamps')
        self.neon = SwitchMRow(self, 'neon', 'Neon', 0, '{:g}', controllerName='lamps')
        self.krypton = SwitchMRow(self, 'krypton', 'Krypton', 0, '{:g}', controllerName='lamps')
        self.argon = SwitchMRow(self, 'argon', 'Argon', 0, '{:g}', controllerName='lamps')
        self.xenon = SwitchMRow(self, 'xenon', 'Xenon', 0, '{:g}', controllerName='lamps')
        self.qth = SwitchMRow(self, 'halogen', 'QTH', 0, '{:g}', controllerName='lamps')
        self.allFiberLamp = SwitchMRow(self, 'allFiberLamp', 'allFiberLamp', 0, '{:g}', controllerName='lamps')

        self.powerFilterwheel = SwitchMRow(self, 'filterwheel', 'Filterwheel', 0, '{:g}', controllerName='lamps')
        self.linewheel = ValueMRow(self, 'linewheel', 'Line Wheel', 1, '{:s}')
        self.qthwheel = ValueMRow(self, 'qthwheel', 'QTH Wheel', 1, '{:s}')
        self.adc1 = ValueMRow(self, 'adc', 'ADC 1', 0, '{:.4f}')
        self.adc2 = ValueMRow(self, 'adc', 'ADC 2', 1, '{:.4f}')

        self.rows = [RowOne(self), RowTwo(self)]

        self.controllers = Controllers(self)
        self.createDialog(DcbDialog(self))

    @property
    def widgets(self):
        return sum([row.widgets for row in self.rows], [])


class DcbDialog(ControlDialog):
    def __init__(self, dcbRow):
        ControlDialog.__init__(self, moduleRow=dcbRow)
        self.designId = DesignId(self)
        self.connectCmd = ConnectCmd(self, ['lamps', 'filterwheel'])

        self.topbar.addWidget(self.designId)
        self.topbar.addLayout(self.connectCmd)

        self.lampsPanel = LampsPanel(self)
        self.filterwheelPanel = FilterwheelPanel(self)
        self.collimatorPanel = CollimatorPanel(self)

        self.tabWidget.addTab(self.lampsPanel, 'Lamps')
        self.tabWidget.addTab(self.filterwheelPanel, 'Filterwheel')
        self.tabWidget.addTab(self.collimatorPanel, 'Collimators')
