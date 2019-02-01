from mamba import describe, included_context, it

NEW_EXPORTED_CONTEXT = 'New Exported Context'

with describe('Real tests'):
    with included_context(NEW_EXPORTED_CONTEXT):
        with it('added example'):
            pass
