from mamba import describe, included_context, it

EXPORTED_CONTEXT = 'Exported Context'

with describe('Real tests'):
    with included_context(EXPORTED_CONTEXT):
        with it('added example'):
            pass
