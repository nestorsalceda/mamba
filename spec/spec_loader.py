import os
import imp

from mamba import describe
from sure import expect

with describe('Loader') as _:

    def it_should_keep_the_same_order_than_written():
        spec = os.path.join(os.path.dirname(__file__), 'fixtures', 'without_inner_contexts.py')
        module = imp.load_source(spec.replace('.py', ''), spec)

        expect(module.specs).to.have.length_of(1)
        expect([spec.name for spec in module.specs[0].specs]).to.be.equal(['first_spec', 'second_spec', 'third_spec'])
