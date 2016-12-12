with description('Fixture#with_ignore_rest_context'):
    with context('this context will be ignored'):
        with it('a normal spec'):
            pass

    with only_context('this context will be ignored because this is not the last only_context'):
        with it('a normal spec'):
            pass

        with it('other normal spec'):
            pass

        with _it('a pending spec'):
            pass

    with context('this context will be ignored too'):
        with it('other normal spec'):
            pass

    with only_context('this context will be executed'):
        with it('a normal spec'):
            pass
