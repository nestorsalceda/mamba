from mamba import shared_context, included_context, describe, it, context

SHARED_CONTEXT = 'Shared Context'

with shared_context(SHARED_CONTEXT):
    with it('first shared'):
        pass


with describe('Real tests'):
    with included_context(SHARED_CONTEXT):
        pass
