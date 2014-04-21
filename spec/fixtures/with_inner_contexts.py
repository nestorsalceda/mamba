with description('Fixture#with_inner_contexts'):
    with it('first example'):
        pass

    with it('second example'):
        pass

    with context('#inner_context'):
        with it('fourth example'):
            pass

    with it('third example'):
        pass
