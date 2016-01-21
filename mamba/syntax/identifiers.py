class MambaIdentifiers(object):
    class EXAMPLE_GROUP(object):
        @property
        def ACTIVE(self):
            return ('description', 'context', 'describe')

        @property
        def PENDING(self):
            return MambaIdentifiers._compute_pending_identifiers(self.ACTIVE)

        @property
        def ALL(self):
            return self.ACTIVE + self.PENDING

    class EXAMPLE(object):
        @property
        def ACTIVE(self):
            return ('it',)

        @property
        def PENDING(self):
            return MambaIdentifiers._compute_pending_identifiers(self.ACTIVE)

        @property
        def ALL(self):
            return self.ACTIVE + self.PENDING

    class HOOK(object):
        @property
        def RUN_ORDERS(self):
            return ('before', 'after')

        @property
        def SCOPES(self):
            return ('all', 'each')

    @staticmethod
    def _compute_pending_identifiers(identifiers):
        return tuple('_' + identifier for identifier in identifiers)
