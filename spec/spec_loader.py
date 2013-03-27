import os
import imp

from mamba import describe, context
from sure import expect

with describe('Loader') as _:

    def it_should_keep_the_same_order_than_written():
        spec = os.path.join(os.path.dirname(__file__), 'fixtures', 'without_inner_contexts.py')
        module = imp.load_source(spec.replace('.py', ''), spec)

        expect(module.specs).to.have.length_of(1)
        expect(module.specs[0].specs).to.have.length_of(3)

        expect(module.specs[0].specs[0].name()).to.be.equal('first_spec')
        expect(module.specs[0].specs[1].name()).to.be.equal('second_spec')
        expect(module.specs[0].specs[2].name()).to.be.equal('third_spec')
