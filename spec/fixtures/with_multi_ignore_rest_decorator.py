with description('Fixture#with_multi_ignore_rest_decorator'):
    with context('this context will be ignored'):
        with it('a normal spec'):
            pass

    with only_context('this context will be executed'):
        with only_it('but this method will be ignored because there are other only_it'):
            pass

        with it('a normal spec'):
            pass

        with it('other normal spec'):
            pass

        with _it('a pending spec'):
            pass

        with only_it('this will be executed'):
            pass

    with context('this context will be ignored too'):
        with it('other normal spec'):
            pass
