#mamba: the definitive testing tool for Python

[![Build Status](https://travis-ci.org/nestorsalceda/mamba.png)](https://travis-ci.org/nestorsalceda/mamba)

mamba is the definitive BDD testing framework for Python. Born under the banner of Behaviour Driven Development.

##Overview

```python

from mamba import describe, context

with describe('mamba'):
    def it_should_be_tested_with_mamba_itself():
        pass

    with context('#features'):
        def it_supports_example_groups():
            pass

        with context('#hooks'):
            def before_all():
                pass

            def before():
                pass

            def after():
                pass

            def after_all():
                pass

    with context('#assertion_framework_agnostic'):
        def it_should_be_usable_with_plain_assertions():
            assert True

        def it_should_be_usable_with_hamcrest_style_assertions():
            assert_that(True, is_(True))

        def it_should_be_usable_with_should_dsl_style_assertions():
            True |should| be(True)

        def it_should_be_usable_with_sure_style_assertions():
            True.should.be.true

            expect(True).to.be.true

    with context('#test_doubles_framework_agnostic'):
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
```


##Contribute

If you'd like to contribute, fork [repository](http://github.com/nestorsalceda/mamba), and send a pull request.
