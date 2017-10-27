# -*- coding: utf-8 -*-

from expects import *

from mamba.settings import Settings

IRRELEVANT_SLOW_TEST_THRESHOLD = 'irrelevant slow test threeshold'
IRRELEVANT_ENABLE_CODE_COVERAGE = 'irrelevant enable code coverage'
IRRELEVANT_NO_COLOR = 'irrelevant no color'


with description(Settings):
    with before.each:
        self.settings = Settings()

    with context('when loading defaults'):
        with it('has 75 millis as slow test threshold'):
            expect(self.settings).to(have_property('slow_test_threshold', equal(0.075)))

        with it('has code coverage disabled by default'):
            expect(self.settings).to(have_property('enable_code_coverage', be_false))

        with it('has no color disabled by default'):
            expect(self.settings).to(have_property('no_color', be_false))

    with context('when setting custom values'):
        with it('sets slow test threshold'):
            self.settings.slow_test_threshold = IRRELEVANT_SLOW_TEST_THRESHOLD

            expect(self.settings).to(have_property('slow_test_threshold', IRRELEVANT_SLOW_TEST_THRESHOLD))

        with it('sets code coverage'):
            self.settings.enable_code_coverage = IRRELEVANT_ENABLE_CODE_COVERAGE

            expect(self.settings).to(have_property('enable_code_coverage', IRRELEVANT_ENABLE_CODE_COVERAGE))

        with it('sets no color'):
            self.settings.no_color = IRRELEVANT_NO_COLOR

            expect(self.settings).to(have_property('no_color', IRRELEVANT_NO_COLOR))
