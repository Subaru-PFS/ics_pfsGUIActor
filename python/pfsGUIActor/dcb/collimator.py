__author__ = 'alefur'

import pfsGUIActor.styles as styles
from PyQt5.QtWidgets import QGroupBox
from ics.utils.instdata import instconfig
from pfsGUIActor.common import GridLayout, ComboBox
from pfsGUIActor.control import ControllerPanel, ControllerCmd, CommandsGB
from pfsGUIActor.widgets import ValueGB, CustomedCmd

nColls = dict(set1=5, set2=5, set3=5, set4=5, oneColl=1)
knownSets = list(nColls.keys())


class MaskCombo(ValueGB):
    fNumbers = ['2.5', '2.8', '3.38']

    def __init__(self, moduleRow, key, ind):
        ValueGB.__init__(self, moduleRow, key=key, title='', ind=ind, fmt='{:s}', fontSize=styles.smallFont)

        self.combo = ComboBox()
        self.combo.addItems(MaskCombo.fNumbers)

        self.hide()

    def setText(self, txt):
        self.combo.setCurrentText(txt[1:])


class BundleCombo(ValueGB):
    names = ['red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'red7', 'red8', 'orange', 'blue', 'green', 'yellow',
             'none']

    def __init__(self, moduleRow, key, ind):
        ValueGB.__init__(self, moduleRow, key=key, title='', ind=ind, fmt='{:s}', fontSize=styles.smallFont)

        self.combo = ComboBox()
        self.combo.addItems(BundleCombo.names)

        self.hide()

    def setText(self, txt):
        self.combo.setCurrentText(txt)


class DeclareMasks(CustomedCmd):
    def __init__(self, collSet):
        self.collSet = collSet
        CustomedCmd.__init__(self, controlPanel=collSet.controlPanel, buttonLabel='SET MASKS')
        self.removeWidget(self.button)

        key = f'coll{collSet.setName.capitalize()}'
        self.masks = [MaskCombo(collSet.controlPanel.moduleRow, f'{key}Masks', i) for i in
                      range(nColls[collSet.setName])]

        for column, mask in enumerate(self.masks):
            self.addWidget(mask.combo, 0, column)
            self.setColumnStretch(column, 2)

        self.addWidget(self.button, 0, len(self.masks))

    def buildCmd(self):
        return f'{self.controlPanel.actorName} declareMasks {self.collSet.setName}={",".join([mask.combo.currentText() for mask in self.masks])}'


class DeclareBundles(CustomedCmd):
    def __init__(self, collSet):
        self.collSet = collSet
        CustomedCmd.__init__(self, controlPanel=collSet.controlPanel, buttonLabel='SET BUNDLES')
        self.removeWidget(self.button)

        key = f'coll{collSet.setName.capitalize()}'
        self.bundles = [BundleCombo(collSet.controlPanel.moduleRow, f'{key}Bundles', i) for i in
                        range(nColls[collSet.setName])]

        for column, bundle in enumerate(self.bundles):
            self.addWidget(bundle.combo, 0, column)
            self.setColumnStretch(column, 2)

        self.addWidget(self.button, 0, len(self.bundles))

    def buildCmd(self):
        return f'{self.controlPanel.actorName} declareBundles {self.collSet.setName}={",".join([bundle.combo.currentText() for bundle in self.bundles])}'


class CollSet(QGroupBox):
    def __init__(self, controlPanel, setName):
        self.setName = setName
        self.controlPanel = controlPanel
        moduleRow = controlPanel.moduleRow
        QGroupBox.__init__(self)
        self.setTitle(f'Collimator {setName}')

        self.grid = GridLayout()
        self.grid.setContentsMargins(*[1, 1, 1, 1])
        self.setLayout(self.grid)

        key = f'coll{setName.capitalize()}'
        masks = [ValueGB(moduleRow, f'{key}Masks', '', i, '{:s}', styles.smallFont) for i in range(nColls[setName])]
        bundles = [ValueGB(moduleRow, f'{key}Bundles', '', i, '{:s}', styles.smallFont) for i in range(nColls[setName])]

        for column, (mask, bundle) in enumerate(zip(masks, bundles)):
            self.grid.addWidget(mask, 0, column)
            self.grid.addWidget(bundle, 1, column)

        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; font-weight: normal; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 0.5ex;} " % styles.smallFont +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")


class CollimatorPanel(ControllerPanel):
    def __init__(self, controlDialog):
        self.setNames = self.loadSetNames(controlDialog.moduleRow.actorName)

        ControllerPanel.__init__(self, controlDialog, 'lamps')
        self.addCommandSet(CollimatorCommands(self))

    def loadSetNames(self, actorName):
        actorConfig = instconfig.InstConfig(actorName)
        setup = actorConfig['illumination']['setup']
        return actorConfig['setups'][setup]

    def createWidgets(self):
        self.collSets = [CollSet(self, setName) for setName in self.setNames]

    def setInLayout(self):
        for i, set in enumerate(self.collSets):
            self.grid.addWidget(set, i, 0, 1, set.grid.columnCount())


class CollimatorCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)

        for i, set in enumerate(controlPanel.collSets):
            self.grid.addLayout(DeclareMasks(set), 2 * i, 0)
            self.grid.addLayout(DeclareBundles(set), 2 * i + 1, 0)

    def addButtons(self, controlPanel):
        pass

    def setEnabled(self, a0: bool):
        CommandsGB.setEnabled(self, a0)
