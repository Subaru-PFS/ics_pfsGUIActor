import pfsGUIActor.dcb as dcb
import pfsGUIActor.lam.aten as lamAten
import pfsGUIActor.lam.breva as lamBreva
import pfsGUIActor.lam.sac as lamSac
import pfsGUIActor.styles as styles
from PyQt5.QtWidgets import QGroupBox
from pfsGUIActor.common import GridLayout, Label, PushButton
from pfsGUIActor.module import Module
from pfsGUIActor.rough import RoughRow
from pfsGUIActor.widgets import ValueGB


class AitModule(Module):
    def __init__(self, mwindow):
        Module.__init__(self, mwindow=mwindow, title='AIT')
        actors = mwindow.actor.displayConfig['ait']

        self.dcbs = []

        if 'dcb' in actors:
            self.dcbs += dcb.DcbRow(self).rows
        if 'dcb2' in actors:
            self.dcbs += dcb.DcbRow(self, 'dcb2').rows

        lamAITRows = []
        lamAITRows += lamAten.AtenRow(self).rows if 'aten' in actors else []
        lamAITRows += [lamSac.SacRow(self)] if 'sac' in actors else []
        lamAITRows += [lamBreva.BrevaRow(self)] if 'breva' in actors else []

        self.lamAITRows = lamAITRows

        roughs = ['rough1'] if 'rough1' in actors else []
        roughs += (['rough2'] if 'rough2' in actors else [])

        self.roughs = [RoughRow(self, rough) for rough in roughs]

        self.populateLayout()

    @property
    def rows(self):
        return self.dcbs + self.roughs + self.lamAITRows


class AitStatus(ValueGB):
    def __init__(self, aitModule):
        QGroupBox.__init__(self)
        self.setTitle('AIT')

        self.grid = GridLayout()
        self.grid.setContentsMargins(5, 0, 0, 0)

        self.value = Label()
        self.grid.addWidget(self.value, 0, 0)

        self.button = PushButton()
        self.button.setFlat(True)
        self.button.clicked.connect(aitModule.showModule)
        self.grid.addWidget(self.button, 0, 0)

        self.setLayout(self.grid)

    def setOnline(self, isOnline):
        self.fontSize = styles.bigFont
        text = 'ONLINE' if isOnline else 'OFFLINE'
        key = text if isOnline else 'failed'
        self.value.setText(text)
        self.setColor(*styles.colorWidget(key))
