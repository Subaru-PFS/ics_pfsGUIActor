__author__ = 'alefur'
import pfsGUIActor.styles as styles
from pfsGUIActor.cam import CamDevice
from pfsGUIActor.common import LineEdit
from pfsGUIActor.control import ControllerCmd
from pfsGUIActor.widgets import ValueGB, SwitchButton, CustomedCmd


class Status(ValueGB):
    maxNb = 2

    def __init__(self, moduleRow):
        ValueGB.__init__(self, moduleRow, 'turboStatus', 'Status', 1, '{:s}')

    def setText(self, txt):
        ftext = [stat for stat in txt.split(',') if 'bit ' not in stat]
        chunks = [','.join(ftext[x:x + Status.maxNb]) for x in range(0, len(ftext), Status.maxNb)]

        self.value.setText('\n'.join(chunks))
        self.customize()


class Speed(ValueGB):
    def __init__(self, moduleRow):
        ValueGB.__init__(self, moduleRow, 'turboSpeed', 'Speed(RPM)', 0, '{:g}')

    def customize(self):

        state = 'on' if float(self.value.text()) > 0 else 'off'
        background, police = styles.colorWidget(state)

        self.setColor(background=background, police=police)
        self.setEnabled(self.moduleRow.isOnline)


class TurboSwitch(SwitchButton):
    def __init__(self, controlPanel):
        cmdHead = '%s turbo' % controlPanel.actorName
        SwitchButton.__init__(self, controlPanel, 'turboSpeed', label='', cmdHead='',
                              cmdStrOn='%s start' % cmdHead, cmdStrOff='%s stop' % cmdHead,
                              labelOn='START', labelOff='STOP', safetyCheck=True)


    def setText(self, txt):
        try:
            speed = int(txt)
            bool = True if speed > 1000 else False
        except ValueError:
            bool = False

        self.buttonOn.setVisible(not bool)
        self.buttonOff.setVisible(bool)


class RawCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='RAW')

        self.rawCmd = LineEdit()
        self.addWidget(self.rawCmd, 0, 1)

    def buildCmd(self):
        cmdStr = '%s turbo raw=%s' % (self.controlPanel.actorName, self.rawCmd.text())
        return cmdStr


class TurboPanel(CamDevice):
    def __init__(self, controlDialog):
        CamDevice.__init__(self, controlDialog, 'turbo')
        self.addCommandSet(TurboCommands(self))

    def createWidgets(self):
        self.speed = Speed(self.moduleRow)
        self.status = Status(self.moduleRow)
        self.volt = ValueGB(self.moduleRow, 'turboVAW', 'Voltage(V)', 0, '{:g}')
        self.current = ValueGB(self.moduleRow, 'turboVAW', 'Current(A)', 1, '{:g}')
        self.power = ValueGB(self.moduleRow, 'turboVAW', 'Power(W)', 2, '{:g}')
        self.bodyTemp = ValueGB(self.moduleRow, 'turboTemps', 'bodyTemp(°C)', 0, '{:g}')
        self.controllerTemp = ValueGB(self.moduleRow, 'turboTemps', 'controllerTemp(°C)', 1, '{:g}')

    def setInLayout(self):
        self.grid.addWidget(self.speed, 0, 0)
        self.grid.addWidget(self.status, 0, 1, 2, 2)
        self.grid.addWidget(self.volt, 2, 0)
        self.grid.addWidget(self.current, 2, 1)
        self.grid.addWidget(self.power, 2, 2)
        self.grid.addWidget(self.bodyTemp, 3, 0)
        self.grid.addWidget(self.controllerTemp, 3, 1)


class TurboCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)

        self.turboSwitch = TurboSwitch(controlPanel=controlPanel)
        self.rawCmd = RawCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.turboSwitch.buttonOn, 1, 0, 1, 2)
        self.grid.addWidget(self.turboSwitch.buttonOff, 1, 0, 1, 2)
        self.grid.addLayout(self.rawCmd, 2, 0, 1, 2)
