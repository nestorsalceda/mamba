from mamba import description, context, it
from unittest import mock
import unittest.mock
from unittest.mock import patch

from expects import expect, be


class ExampleClass(object):

    def hello(self):
        return 'Hello'


with description('Testing with unittest.mock'):

    with context('when class method is mocked'):
        with it('returns mocked value'):
            with patch.object(ExampleClass, 'hello', return_value='World!') as mock_method:
                expect(mock_method()).to(be('World!'))

    with context('when a nested patch attribute is used'):
        with it('runs mock.patch.object context managers'):
            with mock.patch.object(ExampleClass, 'hello', return_value='World!'):
                expect(ExampleClass().hello()).to(be('World!'))

        with it('runs fully qualified patch context managers'):
            with unittest.mock.patch.object(ExampleClass, 'hello', return_value='World!'):
                expect(ExampleClass().hello()).to(be('World!'))
