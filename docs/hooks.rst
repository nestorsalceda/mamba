Hooks
=====

'before' and 'after' hooks
--------------------------

Sometimes several tests shares some code. For avoiding repeating same code over and over, we could use *before* and *after* context manager.

These hooks are executed before or after every example or every example group.


.. code-block:: python

  from mamba import description, before, after, it

  with description('Hooks') as self:

    with before.all:
      # This code is executed once, before executing any examples in this group

    with before.each:
      # This code is executed before every example

    with after.all:
      # This code is executed after all of the examples in this group

    with after.each:
      # This code is executed after each example

A more realistic example would be:

.. code-block:: python

  from mamba import description, before, it

  class Stuff(object):

    def __init__(self):
      self._elements = []

    def elements(self):
      return self._elements

    def add_element(self, element)
      self._elements.append(element)

  with description(Stuff) as self:

    with before.each:
      # Initialize a new stuff for every example
      self.stuff = Stuff()

    with it('has 0 elements'):
      expect(self.stuff.elements()).to(have_length(0))

    with it('accepts elements'):
      self.stuff.add_element(object())

      expect(self.stuff.elements()).to(have_length(1))
