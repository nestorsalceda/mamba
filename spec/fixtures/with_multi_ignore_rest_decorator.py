with description('Fixture#with_multi_ignore_rest_decorator'):
    with context('this context will be executed'):
        with focus_it('but this method will be ignored because there are other focus_it'):
            pass

        with it('a normal spec'):
            pass

        with it('other normal spec'):
            pass

        with _it('a pending spec'):
            pass

        with focus_it('this will be executed'):
            pass
