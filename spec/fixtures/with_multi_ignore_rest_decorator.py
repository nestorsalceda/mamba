with description('Fixture#with_ignore_rest_decorator'):
    with only('ignore rest spec'):
        pass

    with it('a normal spec'):
        pass

    with it('other normal spec'):
        pass

    with _it('a pending spec'):
        pass

    with only('other ignore rest spec'):
        pass
