import logging

import actorcore.ICC
from ics.utils.sps.spectroIds import getSite


class OurActor(actorcore.ICC.ICC):
    def __init__(self, name, productName=None, modelNames=None, configFile=None, logLevel=logging.INFO):
        # This sets up the connections to/from the hub, the logger, and the twisted reactor.
        #
        modelNames = [] if modelNames is None else modelNames
        actorcore.ICC.ICC.__init__(self, name,
                                   productName=productName,
                                   configFile=configFile,
                                   modelNames=modelNames)

        self.site = getSite()
        self.displayConfig = self.actorConfig['display'][self.site]
        self.logger.setLevel(logLevel)

    def disconnectActor(self):
        self.shuttingDown = True


def connectActor(modelNames):
    theActor = OurActor('pfsgui',
                        productName='pfsGUIActor',
                        modelNames=modelNames,
                        logLevel=logging.DEBUG)

    theActor.run(doReactor=False)
    return theActor
