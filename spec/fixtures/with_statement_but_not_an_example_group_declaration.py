with my_custom_context_manager:
    pass

with something():
    pass

with not_an_example_group('this is not an example group declaration'):
    pass

with describe(12):
    pass

with description():
    pass

with context(not 'an example group declaration'):
    pass

with _describe(-11):
    pass

with _description(1 + 2):
    pass

with _context(lambda: 'no, this is not an example group'):
    pass
