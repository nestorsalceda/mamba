from mamba import shared_context, included_context, describe, it

SHARED_CONTEXT = 'Shared Context'

with shared_context(SHARED_CONTEXT):
    with it('shared example'):
        pass


with describe('Real tests'):
    with included_context(SHARED_CONTEXT):
        with it('added example'):
            pass
