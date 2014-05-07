with _description('Fixture#with_pending_decorator_as_root'):

    with it('pending spec'):
        pass

    with context('when pending context'):
        with it('pending spec inside context'):
            pass
