# mamba: the definitive test runner for Python

[![Build Status](https://travis-ci.org/nestorsalceda/mamba.svg)](https://travis-ci.org/nestorsalceda/mamba)
[![Latest PyPI Version](https://img.shields.io/pypi/v/mamba.svg)](https://pypi.python.org/pypi/mamba)


**mamba** is the definitive test runner for Python. Born under the banner of [behavior-driven development](https://en.wikipedia.org/wiki/Behavior-driven_development).

## Installation

To install **mamba**, just run:

```sh
$ pip install mamba
```


## Usage

```sh
$ mamba --help
```

You can also read the [Overview](#overview) and take a look at the [spec](./spec).


## Overview

```python
# Importing mamba is not needed!
# import mamba

with description('mamba'):
    with it('is tested with mamba itself'):
        pass

    with it('supports Python 3'):
        pass

    with context('features'):
        with context('defining example groups'):
            with context('with arbitrary levels of nesting'):
                with it('is supported'):
                    pass

        with context('hooks'):
            with before.all:
                print('This code will be run once, before all examples in this group')

            with before.each:
                print('This code will be run once before each example in this group')

            with after.each:
                print('This code will be run once after each example in this group')

            with after.all:
                print('This code will be run once, after all examples in this group')

        with context('pending tests'):
            with _context('when running pending contexts (marked with an underscore)'):
                with it('will not run any spec under a pending context'):
                    pass

            with _it('will not run pending specs (marked with an underscore)'):
                pass

        with it('highlights slow tests'):
            time.sleep(10)

        with context('when using your code from the tests'):
            with it('supports importing installed modules'):
                pass

            with it('supports importing local, non-installed modules'):
                pass

        with context('code coverage measurement'):
            with it('is performed if you pass `--enable-coverage`'):
                pass

            with it('is performed using `coverage`'):
                # see https://pypi.python.org/pypi/coverage/
                pass

            with it('is configured in a `.coveragerc` file at the root of your project'):
                # see https://coverage.readthedocs.io/en/latest/config.html
                pass


    with context('when writing assertions'):
        with it('does not include an assertion mechanism'):
            pass

        with it('works with virtually any assertion mechanism'):
            pass

        with it('can be used with expects'):
            expect(True).to(be_true)

        with it('can be used with hamcrest'):
            assert_that(True, is_(True))

        with it('can be used with should_dsl'):
            True |should| be(True)

        with it('can be used with sure'):
            True.should.be.true

        with it('can be used with plain assertions'):
            assert True

    with context('when using test doubles'):
        with it('does not include a test doubles library'):
            pass

        with it('works with virtually any test doubles library'):
            pass

        with it('can be used with mockito'):
            stub = mock()
            when(stub).is_usable_with_mockito().thenReturn(True)

            expect(stub.is_usable_with_mockito()).to(be_true)

        with it('can be used with doublex'):
            with Spy() as sender:
                sender.is_usable_with_doublex().returns(True)

            assert_that(sender.is_usable_with_doublex(), is_(True))
            assert_that(sender.is_usable_with_doublex, called())

        with it('can be used with mock'):
            is_usable_with_mock = Mock(return_value=True)

            assert is_usable_with_mock()
```


## Contributing

If you'd like to contribute, fork this [repository](http://github.com/nestorsalceda/mamba) and send a pull request.
