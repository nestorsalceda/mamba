Integration with Other Libraries
================================

Assertion Libraries
-------------------

Mamba is "just" a DSL and a test runner, it does not include any assertion mechanism. It should work with any assertion library.

Although, my **personal preference** is using it with `expects <https://github.com/jaimegildesagredo/expects>`_:

.. code-block:: python

  from mamba import description, it
  from expects import expect, be_equal

  with description('Assertion libraries'):
    with it('can be used with expects'):
      expect(True).to(be_true)


Or do you prefer to use Hamcrest assertions?

.. code-block:: python

  from mamba import description, it
  from hamcrest import assert_that, is_

  with description('Assertion libraries'):
    with it('can be used with hamcrest'):
      assert_that(True, is_(True))


So, you should be able to use mamba with your preferred assertion library: should_dsl, sure or even with plain Python assertions.


Test Doubles Libraries
----------------------

Same that last point here. Mamba does not preescribe any test double library, it should work with any library.

Another time, my **personal preference** is using `Doublex <https://bitbucket.org/DavidVilla/python-doublex>`_ and `doublex-expects <https://github.com/jaimegildesagredo/doublex-expects>`_:

.. code-block:: python

  from mamba import description, it
  from expects import expect
  from doublex import Spy
  from doublex-expects import have_been_called

  with description('Test Doubles Libraries'):
    with it('can be used with doublex'):
      with Spy() as sender:
        sender.is_usable_with_doublex().returns(True)

      mail_gateway = Mailer(sender)
      mail_gateway.send('Hello')

      expect(sender.is_usable_with_doublex).to(have_been_called)

You prefer mockito?

.. code-block:: python

  from mamba import description, it
  from expects import expect, be_true
  from mockito import mock

  with description('Test Doubles Libraries'):
    with it('can be used with mockito'):
      sender = mock()

      when(sender).is_usable_with_mockito().returns(True)

      expect(sender.is_usable_with_mockito()).to(be_true)

So, you can use mamba with your peferred test doubles library too: python mock, or even hand crafted fake objects.
