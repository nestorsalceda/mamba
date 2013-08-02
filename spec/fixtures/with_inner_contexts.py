from mamba import describe, context

with describe('Fixture#with_inner_contexts'):
    def first_example():
        pass

    def second_example():
        pass

    with context('#inner_context'):
        def fourth_example():
            pass

    def third_example():
        pass
