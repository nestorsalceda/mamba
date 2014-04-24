# -*- coding: utf-8 -*-

from expects import expect

from mamba.settings import Settings

IRRELEVANT_SLOW_TEST_THRESHOLD = 'irrelevant slow test threeshold'
IRRELEVANT_ENABLE_CODE_COVERAGE = 'irrelevant enable code coverage'
IRRELEVANT_ENABLE_FILE_WATCHER = 'irrelevant enable file watcher'


with description(Settings):

    with context('when loading defaults'):
        with it('has 75 millis as slow test threshold'):
            expect(self.subject).to.have.property('slow_test_threshold').to.be.equal(0.075)

        with it('has code coverage disabled by default'):
            expect(self.subject).to.have.property('enable_code_coverage').to.be.false

        with it('has file watcher disabled by default'):
            expect(self.subject).to.have.property('enable_file_watcher').to.be.false

    with context('when setting custom values'):
        with it('sets slow test threshold'):
            self.subject.slow_test_threshold = IRRELEVANT_SLOW_TEST_THRESHOLD

            expect(self.subject).to.have.property('slow_test_threshold').to.be.equal(IRRELEVANT_SLOW_TEST_THRESHOLD)

        with it('sets code coverage'):
            self.subject.enable_code_coverage = IRRELEVANT_ENABLE_CODE_COVERAGE

            expect(self.subject).to.have.property('enable_code_coverage').to.be.equal(IRRELEVANT_ENABLE_CODE_COVERAGE)

        with it('sets file watcher'):
            self.subject.enable_file_watcher = IRRELEVANT_ENABLE_FILE_WATCHER

            expect(self.subject).to.have.property('enable_file_watcher').to.be.equal(IRRELEVANT_ENABLE_FILE_WATCHER)
