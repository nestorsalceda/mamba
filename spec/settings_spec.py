# -*- coding: utf-8 -*-

from mamba import describe, context, before
from sure import expect

from mamba.settings import Settings


with describe('Settings') as _:

    with context('when loading defaults'):
        @before.each
        def create_settings():
            _.settings = Settings()

        def it_should_have_75_millis_as_slow_test_threshold():
            expect(_.settings).to.have.property('slow_test_threshold').to.be.equal(0.075)
