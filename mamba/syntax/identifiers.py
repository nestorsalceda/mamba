class _HOOK(object):
    @property
    def RUN_ORDERS(self):
        return ('before', 'after')

    @property
    def SCOPES(self):
        return ('all', 'each')


class _PendingAndActiveIdentifiers(object):
    @property
    def PENDING(self):
        return tuple('_' + identifier for identifier in self.ACTIVE)

    @property
    def ALL(self):
        return self.ACTIVE + self.PENDING


class _EXAMPLE(_PendingAndActiveIdentifiers):
    @property
    def ACTIVE(self):
        return ('it',)


class _EXAMPLE_GROUP(_PendingAndActiveIdentifiers):
    @property
    def ACTIVE(self):
        return ('description', 'context', 'describe')


HOOK = _HOOK()
EXAMPLE = _EXAMPLE()
EXAMPLE_GROUP = _EXAMPLE_GROUP()
