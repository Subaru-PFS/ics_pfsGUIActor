import re


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

    def describe(self):
        return 'Warning(value != OK)'

    def checkAgainstLogic(self, value):
        """Prototype"""
        alertState = 'OK'

        # alert is triggered is value != nominal.
        if value != 'OK':
            alertState = f'{self.keyDescription} : {self.alertFmt.format(value=value)}'

        return alertState


class LimitsW(Warning):
    flavour = 'LimitsW'

    class NoLimit(float):
        def __str__(self):
            return 'None'

    noLowerLimit = NoLimit('-inf')
    noUpperLimit = NoLimit('inf')

    def __init__(self, *args, limits, lowerBoundInclusive, upperBoundInclusive, **kwargs):
        Warning.__init__(self, *args, **kwargs)
        # deactivating boundary constrain if None.
        lowerLimit, upperLimit = limits
        lowerLimit = LimitsW.noLowerLimit if lowerLimit is None else lowerLimit
        upperLimit = LimitsW.noUpperLimit if upperLimit is None else upperLimit

        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit

        self.lowerBoundInclusive = lowerBoundInclusive
        self.upperBoundInclusive = upperBoundInclusive

    def describe(self):
        logic1 = '<=' if self.lowerBoundInclusive else '<'
        logic2 = '<=' if self.upperBoundInclusive else '<'

        if self.lowerLimit != self.noLowerLimit and self.upperLimit == self.noUpperLimit:
            logic1 = logic1.replace('<', '>')
            alertStr = f'value {logic1} {self.lowerLimit}'
        elif self.lowerLimit == self.noLowerLimit and self.upperLimit != self.noUpperLimit:
            alertStr = f'value {logic2} {self.upperLimit}'
        else:
            alertStr = f'{self.lowerLimit} {logic1} value {logic2} {self.upperLimit}'

        return f'Limits({alertStr})'

    def checkAgainstLogic(self, value):
        """Check value against limits."""
        alertState = 'OK'

        lowerBoundOK = value >= self.lowerLimit if self.lowerBoundInclusive else value > self.lowerLimit
        upperBoundOK = value <= self.upperLimit if self.upperBoundInclusive else value < self.upperLimit

        if not (lowerBoundOK and upperBoundOK):
            alertState = self.alertFmt.format(value=value, lowerLimit=self.lowerLimit, upperLimit=self.upperLimit)

        return alertState


class RegexpW(Warning):
    flavour = 'RegexpW'

    def __init__(self, *args, pattern, invert, **kwargs):
        Warning.__init__(self, *args, **kwargs)
        self.pattern = pattern
        self.invert = invert

    def describe(self):
        log = 'not value match' if self.invert else 'value match'
        return f'Regexp({log} {self.pattern})'

    def checkAgainstLogic(self, value):
        """Check value against pattern."""
        alertState = 'OK'
        # alert is triggered is pattern is not matched.
        alertTriggered = re.match(self.pattern, value) is None
        # reverse logic if self.invert==True.
        alertTriggered = not alertTriggered if self.invert else alertTriggered

        if alertTriggered:
            alertState = self.alertFmt.format(value=value)

        return alertState


class BooleanW(Warning):
    flavour = 'BooleanW'

    def __init__(self, *args, nominalValue, **kwargs):
        Warning.__init__(self, *args, **kwargs)
        self.nominalValue = nominalValue

    def describe(self):
        return f'Boolean(value == {self.nominalValue})'

    def checkAgainstLogic(self, value):
        """Check value against nominal value."""
        alertState = 'OK'

        # alert is triggered is value != nominal.
        if value != self.nominalValue:
            alertState = self.alertFmt.format(value=value)

        return alertState


def build(*args, alertType, **alertConfig):
    if alertType == 'trigger':
        return Warning(*args, **alertConfig)
    elif alertType == 'limits':
        return LimitsW(*args, **alertConfig)
    elif alertType == 'regexp':
        return RegexpW(*args, **alertConfig)
    elif alertType == 'boolean':
        return BooleanW(*args, **alertConfig)
    else:
        raise KeyError('unknown alertType')
