# mamba: the definitive test runner for Python

[![Build Status](https://travis-ci.org/nestorsalceda/mamba.svg)](https://travis-ci.org/nestorsalceda/mamba)
[![Latest PyPI Version](https://img.shields.io/pypi/v/mamba.svg)](https://pypi.python.org/pypi/mamba)
[![Read The Docs Status](https://readthedocs.org/projects/pip/badge/)](https://mamba-bdd.readthedocs.io/en/latest/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mamba.svg)](https://pypi.python.org/pypi/mamba/)


**mamba** is the definitive test runner for Python. Born under the banner of [behavior-driven development](https://en.wikipedia.org/wiki/Behavior-driven_development).

## Install

I recommend to use pipenv for managing your dependencies, thus you can install mamba like any other Python package.

By example:

```
  $ pipenv install mamba
```

But you also can use pip:

```
  $ pip install mamba
```


## Getting Started

Write a very simple example that describes your code behaviour:

```python
  # tennis_spec.py

  from mamba import description, context, it
  from expects import expect, equal

  with description('Tennis') as self:
    with it('starts with 0 - 0 score'):
      rafa_nadal = "Rafa Nadal"
      roger_federer = "Roger Federer"
      game = Game(rafa_nadal, roger_federer)

      expect(game.score()).to(equal((0, 0)))
```


Run the example, and don't forget to watch it fail!

```
  $ pipenv run mamba tennis_spec.py

  F

  1 examples failed of 1 ran in 0.0023 seconds

  Failures:

    1) Tennis it starts with 0 - 0 score
      Failure/Error: tennis_spec.py game = Game(rafa_nadal, roger_federer)
          NameError: global name 'Game' is not defined

      File "tennis_spec.py", line 8, in 00000001__it starts with 0 - 0 score--
          game = Game(rafa_nadal, roger_federer)
```

Now write as little code for making it pass.

```python
  # tennis_spec.py

  from mamba import description, context, it
  from expects import expect, equal

  import tennis

  with description('Tennis') as self:
    with it('starts with 0 - 0 score'):
      rafa_nadal = "Rafa Nadal"
      roger_federer = "Roger Federer"
      game = tennis.Game(rafa_nadal, roger_federer)

      expect(game.score()).to(equal((0, 0)))
```

```python
  # tennis.py

  class Game(object):
    def __init__(self, player1, player2):
      pass

    def score(self):
      return (0, 0)
```

Run the spec file and enjoy that all tests are green!

```
  $ pipenv run mamba tennis_spec.py

  .

  1 examples ran in 0.0022 seconds
```

## Settings

Mamba provides a way to configuration using `spec/spec_helper.py` or `specs/spec_helper.py`
This module function is read after parsing arguments so configure function overrides settings

A sample config file :

```python
def configure(settings):
  # settings.slow_test_threshold = 0.075
  # settings.enable_code_coverage = False
  # settings.code_coverage_file = '.coverage'
  settings.format = 'documentation'
  # settings.no_color = False
  # settings.tags = None

```
## Official Manual

You can read more features about mamba in its [official manual](https://mamba-bdd.readthedocs.io/en/latest/)

## Contributors

Here's a [list](https://github.com/nestorsalceda/mamba/graphs/contributors) of all the people who have contributed.

I'm really grateful to each and every of them!

If you want to be one of them, fork [repository](http://github.com/nestorsalceda/mamba) and send a pull request.
