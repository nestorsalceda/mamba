with description('Fixture#with_ignore_rest_decorator'):
    with context('this context will be executed'):
        with it('a normal spec'):
            pass

        with only_it('this method will be executed'):
            pass

        with it('other normal spec'):
            pass

        with _it('a pending spec'):
            pass