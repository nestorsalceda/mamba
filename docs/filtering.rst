Filtering
=========

Sometimes, constraining which examples are run is really useful. Try to think in testing pyramid:

* Unit Tests
* Integration Tests
* End2End Tests

E2E tests are slowest, but integration ones are slower than unit. Perhaps I would like to keep my unit tests running all time, for making the feedback loop shorter, and execute integration tests only a few times before committing.

Mamba supports this use case using tags.

Including examples with a filter
--------------------------------

An inclusion filter is a filter which runs all tests which matches with a tag, let's see an example:

.. code-block:: python

  # customer_repository_spec.py

  from mamba import description, before, it
  from expects import expect, be_equal

  from app import repositories, infrastructure, model

  with description(repositories.CustomerRepository, 'integration') as self:
    with before.each:
      connection = intrastructure.create_connection()
      self.database_cleaner = infrastructure.DatabaseCleaner(connection)
      self.database_cleaner.clean()

      self.repository = repositories.CustomerRepository(connection)


    with it('stores a new customer'):
      customer = model.Customer()

      self.repository.put(customer)
      retrieved = self.repository.find_by_id(customer.id)

      expect(customer).to(be_equal(retrieved))

This is a contract test. It uses database and cleans all records on every execution. Potentially is a bit more expensive than other example which uses a fake-implementation in memory.

.. code-block:: python

  # customer_spec.py

  from mamba import description, before, it
  from expects import expect, be_equal

  from app import model

  with description(model.Customer, 'unit') as self:
    with before.each:
      self.customer = Customer()

    with it('adds orders'):
      customer.add_order(model.Order('Implementing Domain-Driven Design'))

      expect(customer).to(be_equal(retrieved))

So you are able to run all tests:

::

  $ pipenv run mamba

Or run only unit tests:

::

  $ pipenv run mamba -t unit

Or tun only integration tests

::

  $ pipenv run mamba -t integration


You can select the inclusion tag using the -t parameter in command line.

Focused examples
----------------

This is an special case of example inclusion. This allows to focus execution only in an example or an example group. Sometimes you will need to focus execution only in a small piece of code for a while.

.. code-block:: python

  from mamba import description, it, fit

  from katas import MarsRover

  with description(MarsRover) as self:
    with context('when starts at 0, 0 and facing north'):
      with before.each:
        self.mars_rover = MarsRover((0, 0), 'N')

      with it('moves north'):
        self.mars_rover.move('N')

        expect(self.mars_rover.position()).to(be_equal((0, 1))
        expect(self.mars_rover.direction()).to(be_equal('N'))

      # This is the unique example that will be executed
      with fit('moves east'):
        self.mars_rover.move('E')

        expect(self.mars_rover.position()).to(be_equal((1, 0))
        expect(self.mars_rover.direction()).to(be_equal('E'))

So when running this example:

::

  $ pipenv run mamba

  .

  1 examples ran in 0.0014 seconds

It only runs the 'moves east' example. And this could be applied to example groups too, using the *fcontext* context manager.

And please, be kind with your teammates and avoid committing focused example. Eventually they will blame me for this ;)
