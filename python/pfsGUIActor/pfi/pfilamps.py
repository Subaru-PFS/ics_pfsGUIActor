__author__ = 'alefur'

import pfsGUIActor.styles as styles
from pfsGUIActor.common import LineEdit
from pfsGUIActor.control import ControlDialog
from pfsGUIActor.enu import ConnectCmd
from pfsGUIActor.modulerow import ModuleRow, RowWidget
from pfsGUIActor.widgets import ValueMRow, SwitchMRow, Controllers, ValueGB, SwitchGB


class PfiLampsRow(ModuleRow):
    def __init__(self, pfiModule, name='pfilamps'):
        ModuleRow.__init__(self, module=pfiModule, actorName=name, actorLabel=name.upper())

        self.hg = SwitchGB(self, 'HgState', 'Hg', 0, '{:g}')
        self.cd = SwitchGB(self, 'CdState', 'Cd', 0, '{:g}')
        self.neon = SwitchGB(self, 'NeState', 'Neon', 0, '{:g}')
        self.krypton = SwitchGB(self, 'KrState', 'Krypton', 0, '{:g}')
        self.argon = SwitchGB(self, 'ArState', 'Argon', 0, '{:g}')
        self.xenon = SwitchGB(self, 'XeState', 'Argon', 0, '{:g}')
        self.qth = SwitchGB(self, 'ContState', 'QTH', 0, '{:g}')

    @property
    def widgets(self):
        return [self.hg, self.cd, self.neon, self.krypton, self.argon, self.xenon, self.qth]
