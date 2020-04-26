Getting Started
===============

Prerequisites
-------------

Python 3.6 or higher.

Installation
------------

I recommend to use pipenv for managing your dependencies, thus you can install mamba like any other Python package.

By example:

::

  $ pipenv install mamba


But you also can use pip:

::

  $ pip install mamba


Your first example
------------------

Write a very simple example that describes your code behaviour:

.. code-block:: python

  # tennis_spec.py

  from mamba import description, context, it
  from expects import expect, equal

  with description('Tennis') as self:
    with it('starts with 0 - 0 score'):
      rafa_nadal = "Rafa Nadal"
      roger_federer = "Roger Federer"
      game = Game(rafa_nadal, roger_federer)

      expect(game.score()).to(equal((0, 0)))


Run the example, and don't forget to watch it fail!

::

  $ pipenv run mamba tennis_spec.py

  F

  1 examples failed of 1 ran in 0.0023 seconds

  Failures:

    1) Tennis it starts with 0 - 0 score
      Failure/Error: tennis_spec.py game = Game(rafa_nadal, roger_federer)
          NameError: global name 'Game' is not defined

      File "tennis_spec.py", line 8, in 00000001__it starts with 0 - 0 score--
          game = Game(rafa_nadal, roger_federer)


Now write as little code for making it pass.

.. code-block:: python

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


.. code-block:: python

  # tennis.py

  class Game(object):
    def __init__(self, player1, player2):
      pass

    def score(self):
      return (0, 0)


Run the spec file and enjoy that all tests are green!

::

  $ pipenv run mamba tennis_spec.py

  .

  1 examples ran in 0.0022 seconds
