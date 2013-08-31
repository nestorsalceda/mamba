# -*- coding: utf-8 -*-

from mamba import describe, context
from sure import expect

from mamba.settings import Settings

IRRELEVANT_SLOW_TEST_THRESHOLD = 'irrelevant slow test threeshold'
IRRELEVANT_ENABLE_CODE_COVERAGE = 'irrelevant enable code coverage'
IRRELEVANT_ENABLE_FILE_WATCHER = 'irrelevant enable file watcher'


with describe(Settings) as _:
    with context('when loading defaults'):
        def it_has_75_millis_as_slow_test_threshold():
            expect(_.subject).to.have.property('slow_test_threshold').to.be.equal(0.075)

        def it_has_code_coverage_disabled_by_default():
            expect(_.subject).to.have.property('enable_code_coverage').to.be.false

        def it_has_file_watcher_disabled_by_default():
            expect(_.subject).to.have.property('enable_file_watcher').to.be.false

    with context('when setting custom values'):
        def it_sets_slow_test_threshold():
            _.subject.slow_test_threshold = IRRELEVANT_SLOW_TEST_THRESHOLD

            expect(_.subject).to.have.property('slow_test_threshold').to.be.equal(IRRELEVANT_SLOW_TEST_THRESHOLD)

        def it_sets_code_coverage():
            _.subject.enable_code_coverage = IRRELEVANT_ENABLE_CODE_COVERAGE

            expect(_.subject).to.have.property('enable_code_coverage').to.be.equal(IRRELEVANT_ENABLE_CODE_COVERAGE)

        def it_sets_file_watcher():
            _.subject.enable_file_watcher = IRRELEVANT_ENABLE_FILE_WATCHER

            expect(_.subject).to.have.property('enable_file_watcher').to.be.equal(IRRELEVANT_ENABLE_FILE_WATCHER)
