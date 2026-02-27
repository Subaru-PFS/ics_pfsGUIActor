__author__ = 'alefur'

from pfsGUIActor.control import ControlDialog
from pfsGUIActor.modulerow import ModuleRow, RowWidget
from pfsGUIActor.widgets import ValueMRow


class PfsDesignRow(RowWidget):
    def __init__(self, iicRow):
        RowWidget.__init__(self, iicRow)

        self.designId = ValueMRow(self.moduleRow, 'pfsDesign', 'pfsDesignId', 0, '0x{:016x}')
        self.raBoresight = ValueMRow(self.moduleRow, 'pfsDesign', 'raBoresight', 2, '{:.5f}')
        self.decBoresight = ValueMRow(self.moduleRow, 'pfsDesign', 'decBoresight', 3, '{:.5f}')
        self.posAng = ValueMRow(self.moduleRow, 'pfsDesign', 'posAng', 4, '{:.5f}')
        self.designName = ValueMRow(self.moduleRow, 'pfsDesign', 'designName', 5, '{:s}')

    @property
    def widgets(self):
        return [self.designId, self.designName, self.raBoresight, self.decBoresight, self.posAng]


class PfsConfigRow(RowWidget):
    def __init__(self, iicRow):
        RowWidget.__init__(self, iicRow)

        self.designId = ValueMRow(self.moduleRow, 'pfsConfig', 'pfsConfigId', 0, '0x{:016x}')
        self.visit = ValueMRow(self.moduleRow, 'pfsConfig', 'visitId', 1, '{:d}')
        self.visit0 = ValueMRow(self.moduleRow, 'pfsConfig', 'visit0', 2, '{:d}')
        self.dateDir = ValueMRow(self.moduleRow, 'pfsConfig', 'dateDir', 3, '{:s}')
        self.raBoresight = ValueMRow(self.moduleRow, 'pfsConfig', 'raBoresight', 4, '{:.5f}')
        self.decBoresight = ValueMRow(self.moduleRow, 'pfsConfig', 'decBoresight', 5, '{:.5f}')
        self.posAng = ValueMRow(self.moduleRow, 'pfsConfig', 'posAng', 6, '{:.5f}')
        self.designName = ValueMRow(self.moduleRow, 'pfsConfig', 'designName', 7, '{:s}')

    @property
    def widgets(self):
        return [self.designId, self.visit, self.visit0, self.dateDir, self.raBoresight, self.decBoresight, self.posAng,
                self.designName]

    @property
    def displayed(self):
        return [None, self.designId, self.designName, self.dateDir, self.visit, self.visit0]


class IicRow(ModuleRow):
    def __init__(self, iicModule):
        ModuleRow.__init__(self, module=iicModule, actorName='iic', actorLabel='IIC')

        self.rows = [PfsDesignRow(self), PfsConfigRow(self)]

        self.createDialog(IicDialog(self))

    @property
    def widgets(self):
        return sum([row.widgets for row in self.rows], [])


class IicDialog(ControlDialog):
    def __init__(self, iicRow):
        ControlDialog.__init__(self, moduleRow=iicRow, title='IIC')
