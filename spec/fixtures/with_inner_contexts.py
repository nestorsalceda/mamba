from mamba import describe, context

with describe('Fixture#with_inner_contexts'):
    def first_spec():
        pass

    def second_spec():
        pass

    with context('#inner_context'):
        def fourth_spec():
            pass

    def third_spec():
        pass
