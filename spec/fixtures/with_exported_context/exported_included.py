from mamba import shared_context, included_context, describe, it, exported_context

EXPORTED_CONTEXT = 'Exported Context'
NEW_EXPORTED_CONTEXT = 'New Exported Context'

with exported_context(NEW_EXPORTED_CONTEXT):
    with included_context(EXPORTED_CONTEXT):
        pass
    with it('new exported example'):
        pass
