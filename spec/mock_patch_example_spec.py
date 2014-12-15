try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from expects import *


class ExampleClass(object):

    def hello(self):
        return 'Hello'


with description('Testing with unittest.mock'):

    with context('when class method is mocked'):
        with it('returns mocked value'):
            with patch.object(ExampleClass, 'hello', return_value='World!') as mock_method:
                expect(mock_method()).to(be('World!'))


