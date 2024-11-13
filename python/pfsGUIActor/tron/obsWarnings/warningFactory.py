class Warning(object):
    def __init__(self, keyDescription, call=True, alertFmt=None):
        self.keyDescription = keyDescription
        self.call = call
        self.alertFmt = alertFmt

        self.activated = True

    def check(self, value):
        """Overriden by OK if deactivated."""
        if not self.activated:
            return 'OK'

        return self.checkAgainstLogic(value)

    def checkAgainstLogic(self, value):
        """Prototype"""
        alertState = 'OK'

        # alert is triggered is value != nominal.
        if value != 'OK':
            alertState = f'{self.keyDescription} : {self.alertFmt.format(value=value)}'

        return alertState


def build(*args, alertType, **alertConfig):
    if alertType == 'trigger':
        return Warning(*args, **alertConfig)
    else:
        raise KeyError('unknown alertType')
