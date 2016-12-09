with description('Fixture#with_multi_ignore_rest_decorator'):
    with only_context('this context will be executed'):
        with only_it('ignore rest spec'):
            pass

        with it('a normal spec'):
            pass

        with it('other normal spec'):
            pass

        with _it('a pending spec'):
            pass

        with only_it('other ignore rest spec'):
            pass

    with context('this context will be ignored'):
        with it('other normal spec'):
            pass
