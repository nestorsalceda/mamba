from mamba import shared_context, included_context, describe, it, exported_context

EXPORTED_CONTEXT = 'Exported Context'

with exported_context(EXPORTED_CONTEXT):
    with it('exported example'):
        pass
