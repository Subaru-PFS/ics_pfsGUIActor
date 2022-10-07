__author__ = 'alefur'

import pfsGUIActor.styles as styles
from PyQt5.QtWidgets import QGroupBox, QLabel, QDial, QWidget
from pfsGUIActor.common import GridLayout, HBoxLayout
from pfsGUIActor.tron.alerts import AlertsRow
from pfsGUIActor.widgets import ValueGB


class TronDial(QDial):
    style = ''' QDial{background-color:QLinearGradient(x1: 0.177, y1: 0.004, x2: 0.831, y2: 0.911,  stop: 0 white,
    stop: 0.061 white, stop: 0.066 lightgray, stop: 0.5 #242424, stop: 0.505 #000000,stop: 0.827 #040404,
    stop: 0.966 #292929,stop: 0.983 #2e2e2e); }'''

    def __init__(self):
        QDial.__init__(self)
        self.setMinimum(0)
        self.setMaximum(10)
        self.setValue(0)
        self.setMaximumSize(30, 30)
        self.setWrapping(True)  # Smooth transition from 99 to 0
        self.setNotchesVisible(True)
        self.setStyleSheet(self.style)

    def heartBeat(self):
        value = self.value() + 1
        value = 0 if value > self.maximum() else value
        self.setValue(value)


class TronModule(QWidget):
    def __init__(self, mwindow):
        QWidget.__init__(self, mwindow)
        hbox = HBoxLayout()

        self.mwindow = mwindow
        self.tronStatus = TronStatus()
        self.alertsRow = AlertsRow(self)

        hbox.addWidget(self.tronStatus)
        hbox.addWidget(self.alertsRow.status)
        self.setLayout(hbox)

    def setEnabled(self, bool):
        for widget in [self.tronStatus, self.alertsRow]:
            widget.setOnline(bool)


class TronStatus(ValueGB):
    def __init__(self, fontSize=styles.smallFont):
        self.fontSize = fontSize

        QGroupBox.__init__(self)
        self.setTitle('TRON')

        self.grid = GridLayout()
        self.grid.setContentsMargins(5, 0, 0, 0)

        self.value = QLabel()
        self.dial = TronDial()

        self.grid.addWidget(self.value, 0, 0)
        self.grid.addWidget(self.dial, 0, 1)
        self.setLayout(self.grid)

    def setOnline(self, isOnline):
        text = 'ONLINE' if isOnline else 'OFFLINE'
        key = text if isOnline else 'failed'
        self.value.setText(text)
        self.setColor(*styles.colorWidget(key))
