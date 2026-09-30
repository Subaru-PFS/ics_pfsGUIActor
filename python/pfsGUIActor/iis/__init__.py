__author__ = 'alefur'

from pfsGUIActor.modulerow import RowWidget
from pfsGUIActor.pfi.pfilamps import PfiLampsRow


class IisLampsRow(RowWidget):
    def __init__(self, iisRow, lamps, withActor=True):
        RowWidget.__init__(self, iisRow)
        self.lamps = lamps
        self.withActor = withActor

    @property
    def widgets(self):
        return self.lamps

    @property
    def displayed(self):
        return [self.moduleRow.actorStatus if self.withActor else None] + self.lamps


class IisRow(PfiLampsRow):
    lampKeys = ['halogen', 'neon', 'argon', 'krypton', 'hgar', 'hydrogen', 'helium']
    lampsPerRow = 4

    def __init__(self, module):
        PfiLampsRow.__init__(self, module, name='iis')

        self.rows = [IisLampsRow(self, self.lamps[i:i + self.lampsPerRow], withActor=i == 0)
                     for i in range(0, len(self.lamps), self.lampsPerRow)]
