from mamba import shared_context, it

with shared_context('Shared Context'):
    with it('example'):
        pass
