__author__ = 'alefur'

import argparse
import os
import pwd
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from mainwindow import PfsWidget


class PFSGUI(QMainWindow):
    def __init__(self, reactor, actor, cmdrName, screen):
        QMainWindow.__init__(self)
        self.reactor = reactor
        self.actor = actor
        self.actor.connectionMade = self.connectionMade
        self.setName("%s.%s" % ("pfsGUIActor", cmdrName))
        self.isConnected = False
        self.screenWidth = screen.width()
        self.screenHeight = screen.height()
        self.pfsWidget = PfsWidget(self)
        self.setCentralWidget(self.pfsWidget)

        self.show()
        self.move(self.screenWidth * 0.1, self.screenHeight * 0.1)
        self.setConnected(False)

    def setConnected(self, isConnected):
        self.isConnected = isConnected
        self.pfsWidget.setEnabled(isConnected)

    def connectionMade(self):
        """ For overriding. """
        self.setConnected(True)
        self.actor.cmdr.connectionLost = self.connectionLost

    def connectionLost(self, reason):
        """ For overriding. """
        self.setConnected(False)
        if not self.actor.shuttingDown:
            self.pfsWidget.showError("Connection Lost", f"Connection to tron has failed : \n{reason}")

    def setName(self, name):
        self.cmdrName = name
        self.setWindowTitle(name)

    def closeEvent(self, QCloseEvent):
        self.actor.disconnectActor()
        self.reactor.callFromThread(self.reactor.stop)
        QCloseEvent.accept()


def main():
    app = QApplication(sys.argv)
    screen = app.desktop().screenGeometry()
    parser = argparse.ArgumentParser()

    parser.add_argument('--name', default=pwd.getpwuid(os.getuid()).pw_name, type=str, nargs='?', help='cmdr name')

    args = parser.parse_args()

    import qt5reactor

    qt5reactor.install()
    from twisted.internet import reactor

    import miniActor

    specIds = [i + 1 for i in range(4)]
    specIdsWithJHU = specIds + [8, 9]
    viscamNames = ['b%i' % i for i in specIdsWithJHU] + ['r%i' % i for i in specIdsWithJHU]
    nircamNames = ['n%i' % i for i in specIdsWithJHU]

    xcus = ['xcu_%s' % cam for cam in viscamNames + nircamNames]
    ccds = ['ccd_%s' % cam for cam in viscamNames]
    hxs = ['hx_%s' % cam for cam in nircamNames]
    enus = ['enu_sm%i' % i for i in specIds]
    lam = ['aten', 'sac', 'breva']
    sps = ['sps', 'dcb', 'dcb2', 'rough1', 'rough2']
    pfi = ['peb', 'pfilamps']

    actor = miniActor.connectActor(['hub', 'alerts', 'iic'] + lam + sps + enus + xcus + ccds + hxs + pfi)

    try:
        ex = PFSGUI(reactor, actor, args.name, screen)
    except:
        actor.disconnectActor()
        raise

    reactor.run()
    actor.disconnectActor()


if __name__ == "__main__":
    main()
