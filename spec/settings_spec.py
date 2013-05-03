# -*- coding: utf-8 -*-

from mamba import describe, context, before
from sure import expect

from mamba.settings import Settings

IRRELEVANT_SLOW_TEST_THRESHOLD = '0.1'


with describe('Settings') as _:
    @before.each
    def create_settings():
        _.settings = Settings()

    with context('when loading defaults'):
        def it_should_have_75_millis_as_slow_test_threshold():
            expect(_.settings).to.have.property('slow_test_threshold').to.be.equal(0.075)

    with context('when setting custom values'):
        def it_should_set_slow_test_threshold():
            _.settings.slow_test_threshold = IRRELEVANT_SLOW_TEST_THRESHOLD

            expect(_.settings).to.have.property('slow_test_threshold').to.be.equal(IRRELEVANT_SLOW_TEST_THRESHOLD)
