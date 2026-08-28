__author__ = 'alefur'

import numpy as np
import pfsGUIActor.styles as styles
from pfsGUIActor.cam import CamDevice
from pfsGUIActor.control import ControllerCmd, ControlPanel
from pfsGUIActor.widgets import ValueGB, ValuesRow


def irpFromReadTime(readTime, IRP0_READ_TIME=5.6129, IRP1_READ_TIME=10.8570, tolerance=0.05):
    """Return the IRP mode matching readTime, as a displayable string.

    An IRP-N read interleaves one reference pixel every N data pixels, so
    readTime = IRP0_READ_TIME + (IRP1_READ_TIME - IRP0_READ_TIME) / N.

    Parameters
    ----------
    readTime : `float`
        Measured read time, seconds.
    IRP0_READ_TIME, IRP1_READ_TIME : `float`
        Read times, seconds, with IRP off and with IRP1.
    tolerance : `float`
        Read time slack, seconds: widens the accepted range at both ends, and
        is the excess below which the read is declared IRP0. It therefore caps
        the largest reportable ratio.

    Returns
    -------
    irp : `str`
        'IRP{N}', 'IRP0' for a read without reference pixels, or 'nan' when
        readTime is undefined or falls outside the IRP0 to IRP1 range.
    """
    if np.isnan(readTime) or not IRP0_READ_TIME - tolerance < readTime < IRP1_READ_TIME + tolerance:
        return 'nan'

    overhead = readTime - IRP0_READ_TIME
    if overhead < tolerance:
        irp = 0
    else:
        irp = int(round((IRP1_READ_TIME - IRP0_READ_TIME) / overhead))

    return f'IRP{irp:d}'


class RampConfig(ValuesRow):
    labels = ['nRamp', 'nGroup', 'nReset', 'nRead', 'nDrop']

    def __init__(self, moduleRow, fontSize=styles.smallFont):
        widgets = [ValueGB(moduleRow, 'ramp', lab, i, '{:d}') for i, lab in enumerate(RampConfig.labels)]
        ValuesRow.__init__(self, widgets, title='rampConfig', fontSize=fontSize)
        self.grid.setContentsMargins(1, 8, 1, 1)


class HxRead(ValuesRow):
    labels = ['visit', 'nRamp', 'nGroup', 'nRead']

    def __init__(self, moduleRow, fontSize=styles.smallFont):
        widgets = [ValueGB(moduleRow, 'hxread', lab, i, '{:d}') for i, lab in enumerate(HxRead.labels)]
        ValuesRow.__init__(self, widgets, title='HxRead', fontSize=fontSize)


class IRP(ValueGB):
    def __init__(self, moduleRow, fontSize=styles.smallFont):
        super().__init__(moduleRow, 'readTime', '', 0, '{:.3f}', fontSize=fontSize)

    def setText(self, readTime):
        txt = irpFromReadTime(float(readTime))
        self.value.setText(txt)
        self.customize()


class HxPanel(CamDevice):

    def __init__(self, controlDialog):
        # There is hxhal controller but the logic is quite different from the other controllers.
        CamDevice.__init__(self, controlDialog, controllerName='')
        self.addCommandSet(HxCommands(self))

    def createWidgets(self):
        self.rampConfig = RampConfig(self.moduleRow)
        self.hxRead = HxRead(self.moduleRow)
        self.readTime = ValueGB(self.moduleRow, 'readTime', 'readTime', 0, '{:.3f}')
        self.IRP = IRP(self.moduleRow)
        self.filename = ValueGB(self.moduleRow, 'filename', 'filepath', 0, '{:s}')

    def setInLayout(self):
        self.grid.addWidget(self.rampConfig, 0, 0, 1, 5)
        self.grid.addWidget(self.hxRead, 1, 0, 1, 4)
        self.grid.addWidget(self.readTime, 2, 0, 1, 1)
        self.grid.addWidget(self.IRP, 2, 1, 1, 1)
        self.grid.addWidget(self.filename, 3, 0, 1, 3)

    def setEnabled(self, a0):
        connected = self.moduleRow.isOnline
        return ControlPanel.setEnabled(self, connected)


class HxCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)

    def setEnabled(self, a0: bool):
        """Just disable connect / disconnect."""
        super().setEnabled(a0)
        self.connectButton.setEnabled(False)
        self.connectButton.setVisible(False)
        self.disconnectButton.setEnabled(False)
        self.disconnectButton.setVisible(True)
