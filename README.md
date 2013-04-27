#mamba: the definitive testing tool for Python

[![Build Status](https://travis-ci.org/nestorsalceda/mamba.png)](https://travis-ci.org/nestorsalceda/mamba)

mamba is the definitive BDD testing framework for Python. Born under the banner of Behaviour Driven Development.

##Overview

```python

from mamba import describe, context, before, after, skip

with describe('mamba'):
    def it_should_be_tested_with_mamba_itself():
        pass

    with context('when listing features'):
        def it_supports_example_groups():
            pass

        with context('hooks'):
            @before.all
            def run_once_before_specs():
                pass

            @before.each
            def run_before_every_spec():
                pass

            @after.each
            def run_after_every_spec():
                pass

            @after.all
            def run_after_all_specs():
                pass

        with context('skip tests'):
            with skip(context('#skipped contexts')):
                def it_should_not_run_specs_under_a_skipped_context():
                    pass

            @skip
            def it_should_not_run_a_spec_marked_with_skip_decorator():
                pass

    with context('when writing assertions'):
        def it_should_be_usable_with_plain_assertions():
            assert True

        def it_should_be_usable_with_hamcrest_style_assertions():
            assert_that(True, is_(True))

        def it_should_be_usable_with_should_dsl_style_assertions():
            True |should| be(True)

        def it_should_be_usable_with_sure_style_assertions():
            True.should.be.true

            expect(True).to.be.true

        def it_should_be_assertion_framework_agnostic():
            pass

    with context('when using tests doubles'):
        def it_should_be_usable_with_mockito():
            stub = mock()
            when(stub).is_usable_with_mockito().thenReturn(True)

            expect(stub.is_usable_with_mockito()).to.be.true

        def it_should_be_usable_with_doublex():
            with Spy() as sender:
                sender.is_usable_with_doublex().returns(True)

            assert_that(sender.is_usable_with_doublex(), is_(True))
            assert_that(sender.is_usable_with_doublex, called())

        def it_should_be_usable_with_mock():
            is_usable_with_mock = Mock(return_value=True)

            assert mock()

        def it_should_be_test_doubles_framework_agnostic():
            pass
```


##Contribute

If you'd like to contribute, fork [repository](http://github.com/nestorsalceda/mamba), and send a pull request.
