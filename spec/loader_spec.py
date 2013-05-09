import os
import imp

from mamba import describe, context, before
from sure import expect

with describe('Loader') as _:

    def it_should_order_by_line_number_without_inner_context():
        spec = os.path.join(os.path.dirname(__file__), 'fixtures', 'without_inner_contexts.py')
        module = imp.load_source(spec.replace('.py', ''), spec)

        expect(module.specs).to.have.length_of(1)
        expect([spec.name for spec in module.specs[0].specs]).to.be.equal(['first_spec', 'second_spec', 'third_spec'])

    def it_should_put_specs_together_and_groups_at_the_end():
        spec = os.path.join(os.path.dirname(__file__), 'fixtures', 'with_inner_contexts.py')
        module = imp.load_source(spec.replace('.py', ''), spec)

        expect(module.specs).to.have.length_of(1)
        expect([spec.name for spec in
            module.specs[0].specs]).to.be.equal(['first_spec', 'second_spec', 'third_spec', '#inner_context'])

    with context('when a skip decorator loaded'):
        @before.all
        def load_fixture_with_skipped_decorator():
            spec = os.path.join(os.path.dirname(__file__), 'fixtures', 'with_skip_decorator.py')
            _.module = imp.load_source(spec.replace('.py', ''), spec)

        def it_should_mark_spec_as_skipped():
            expect(_.module.specs).to.have.length_of(1)
            expect(_.module.specs[0].specs[0].skipped).to.be.true

        def it_should_mark_spec_group_as_skipped():
            expect(_.module.specs).to.have.length_of(1)
            expect(_.module.specs[0].specs[1].skipped).to.be.true
