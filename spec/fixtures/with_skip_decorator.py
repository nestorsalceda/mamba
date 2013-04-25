from mamba import describe, context, skip

with describe('Fixture#with_skip_decorator'):
    @skip
    def skipped_spec():
        pass

    with skip(context('when skipped context')):
        pass
