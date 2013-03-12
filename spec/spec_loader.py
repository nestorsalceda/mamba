import os
import imp

from mamba import describe, context
from hamcrest import *

with describe('Loader') as _:

    def it_should_keep_the_same_order_than_written():
        spec = os.path.join(os.path.dirname(__file__), 'fixtures', 'without_inner_contexts.py')
        module = imp.load_source(spec.replace('.py', ''), spec)

        assert_that(module.specs, has_length(1))
        assert_that(module.specs[0].specs, has_length(3))

        assert_that(module.specs[0].specs[0].name(), is_('first_spec'))
        assert_that(module.specs[0].specs[1].name(), is_('second_spec'))
        assert_that(module.specs[0].specs[2].name(), is_('third_spec'))
