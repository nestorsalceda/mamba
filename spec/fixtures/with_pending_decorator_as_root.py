from mamba import describe, context, pending

with pending(describe('Fixture#with_pending_decorator_as_root')):

    def pending_spec():
        pass

    with context('when pending context'):

        def pending_spec_inside_context():
            pass
