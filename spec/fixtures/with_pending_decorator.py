from mamba import describe, context, pending

with describe('Fixture#with_pending_decorator'):
    @pending
    def pending_spec():
        pass

    with pending(context('when pending context')):
        pass
