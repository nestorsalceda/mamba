Example Groups
==============

Basic structure (description / it)
----------------------------------

Mamba is an internal Python DSL for creating executable examples.

Mamba organizes execution around example groups, and tries to use a human like languge for expressing behaviour. Like a human conversation.


.. code-block:: python

  from mamba import description, context, it

  with description('A topic') as self:
    with context('when more context is given'):
      with it('happens some stuff and I can check it'):
        value = 'hello'
        other = 'world'

        assert value != other

Mamba uses context managers for organizing the code, so the let's see the about these context managers:

* description: Creates a new example group.
* context: Is basically an alias to description, and also creates an example group. But its usage is restricted to nested example groups.
* it: Creates a new example. Code inside it, will be executed as a test.

Internally, mamba parses this code using the Python ast module, and generates a class for every example group and a method for every example. And executes these classes like unittest (by example!).

Helper methods
--------------

For supporting a nice experience writing examples, mamba allows defining helper methods.

.. code-block:: python

  from mamba import description, context, it

  with description('Refactoring Goodies') as self:
      with it('allows calling a defined method inside the example group'):
        assert self.hello('python') != self.hello('pandas')

      def hello(self, world):
        return 'hello, %s'.format(world)

You can define a helper method using Python language structures. And these helpers are exposed to example in the same group and in nested groups within that group, but not on parents or sibling groups.

Pending examples
----------------

Sometimes I've found myself keeping a small ToDo record about what should test next. Or perhaps we need to disable an specific test.

Mamba supports these cases using pending examples:

.. code-block:: python

  from mamba import description, _it

  with description('Pending Examples') as self:
      with _it('will not run any pending example (marked with an underscore)'):
        assert False


When running this spec, we get the following output:

::

  *

  0 examples ran (1 pending) in 0.0003 seconds


And this also works with example groups:

.. code-block:: python

  from mamba import description, _context, it

  with description('Pending Examples') as self:
      with _context('when running a pending context (marked with an underscore)'):
        with it('will not run any example under a pending context'):
          assert False

        with it('will not be run either'):
          assert False


And when executing this spec:

::

  **

  0 examples ran (2 pending) in 0.0005 seconds

Shared contexts
---------------

In order to `DRY <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_ up your specs it is possible to define shared contexts.

.. code-block:: python

  from mamba import shared_context, it

  with shared_context('Shared store examples'):
      with it('can retrieve stored items'):
          item = {'name': 'Bob'}
          self.store.add(id=1, item=item)

          assert self.store.get(id=1) == item

The examples in a shared context are not executed. You need to include the context by using the `included_context` context manager with the exact same description as the defined shared context.

.. code-block:: python

  from mamba import shared_context, included_context, it, before, describe

  from app.store import InMemoryStore, SQLStore

  with shared_context('Shared store examples'):
      with it('can retrieve stored items'):
          item = {'name': 'Bob'}
          self.store.add(id=1, item=item)

          assert self.store.get(id=1) == item

  with describe(InMemoryStore):
      with before.each:
          self.store = InMemoryStore()

      with included_context('Shared store examples'):
          pass

  with describe(SQLStore):
      with before.each:
          self.store = SQLStore(host='localhost')

       with included_context('Shared store examples'):
          pass

Any examples and example groups defined inside the `included_context` block are **added** to the ones of the previously defined context.
Any hooks defined inside the `included_context` **overwrite** those defined in the `shared_context`.
