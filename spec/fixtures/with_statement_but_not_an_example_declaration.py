with my_custom_context_manager:
    pass

with something():
    pass

with wrong_example('whatever'):
    pass

with it(42):
    pass

with it(False):
    pass

with _it(-3.6):
    pass

with _it(lambda: 'no, this is wrong'):
    pass
