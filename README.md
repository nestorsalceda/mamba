#mamba: the definitive testing tool for Python

[![Build Status](https://travis-ci.org/nestorsalceda/mamba.svg)](https://travis-ci.org/nestorsalceda/mamba)

mamba is the definitive BDD testing framework for Python. Born under the banner of Behavior Driven Development.

##Installation

To install mamba, just:

``` sh
pip install mamba
```

##Overview

```python


with description('mamba'):
    with it('is tested with mamba itself'):
        pass

    with it('supports python 3'):
        pass

    with context('when listing features'):
        with it('supports example groups'):
            pass

        with context('hooks'):
            with before.all:
                print 'This code will be run once, before all examples'

            with before.each:
                print 'This code will be run before each example'

            with after.each:
                print 'This code will be run after each example'

            with after.all:
                print 'This code will be run once, after all examples'

        with context('pending tests'):
            with _context('when running pending contexts (marked with a underscore)'):
                with it('will not run any spec under a pending context'):
                    pass

            with _it('will not run pending specs (marked with underscore)'):
                pass

        with it('highlights slow tests'):
            sleep(10)

        with context(ASampleClass):
            with it('has an instance in subject property'):
                expect(self.subject).to.be.a(ASampleClass)

    with context('when writing assertions'):
        with it('can be used with plain assertions'):
            assert True

        with it('can be used with hamcrest style assertions'):
            assert_that(True, is_(True))

        with it('can be used with should_dsl style assertions'):
            True |should| be(True)

        with it('can be used with sure style assertions'):
            True.should.be.true

            expect(True).to.be.true

        with it('is assertion framework agnostic'):
            pass

    with context('when using tests doubles'):
        with it('can be used with mockito'):
            stub = mock()
            when(stub).is_usable_with_mockito().thenReturn(True)

            expect(stub.is_usable_with_mockito()).to.be.true

        with it('can be used with doublex'):
            with Spy() as sender:
                sender.is_usable_with_doublex().returns(True)

            assert_that(sender.is_usable_with_doublex(), is_(True))
            assert_that(sender.is_usable_with_doublex, called())

        with it('can be used with mock'):
            is_usable_with_mock = Mock(return_value=True)

            assert mock()

        with it('is test doubles framework agnostic'):
            pass

```


##Contribute

If you'd like to contribute, fork [repository](http://github.com/nestorsalceda/mamba), and send a pull request.
