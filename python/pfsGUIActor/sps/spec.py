__author__ = 'alefur'

import pfsGUIActor.styles as styles
from pfsGUIActor.common import PushButton
from pfsGUIActor.widgets import ValueGB, ValueMRow


class SpecLabel(ValueGB):
    def __init__(self, spsRow, specNum):
        self.specNum = specNum
        self.specModule = False
        self.lightSource = ValueMRow(spsRow, f'sm{specNum}LightSource', '', 0, '{:s}')
        self.lightSource.hide()
        self.lightSource.setText = self.setLightSource

        ValueGB.__init__(self, spsRow, 'specModules', '', 0, '{:s}', fontSize=styles.bigFont)

        self.setText(self.specName.upper())

        self.button = PushButton()
        self.button.setFlat(True)
        self.grid.addWidget(self.button, 0, 0)

    @property
    def specName(self):
        return f'sm{self.specNum}'

    def updateVals(self, ind, fmt, keyvar):
        self.updateWidgets(keyvar.getValue(doRaise=False))

    def updateWidgets(self, specModules=None):
        specModules = self.keyvar.getValue(doRaise=False) if specModules is None else specModules
        self.setEnabled(isOnline=self.specName in specModules)

    def connect(self, specModule):
        self.specModule = specModule
        self.button.clicked.connect(specModule.showModule)

    def setEnabled(self, isOnline):
        if isOnline:
            self.setColor(*styles.colorWidget('online'))
        else:
            self.setColor(*styles.colorWidget('offline'))

    def setLightSource(self, lightSource):
        if not self.specModule:
            return

        self.specModule.setTitle(f'Spectrograph Module {self.specNum}   -   {lightSource.upper()}')
