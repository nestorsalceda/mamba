# -*- coding: utf-8 -*-

from mamba import settings, formatters, reporter, runners, example_collector


class ApplicationFactory(object):

    def __init__(self, arguments):
        self._instances = {}
        self.arguments = arguments

    def create_settings(self):
        settings_ = settings.Settings()
        settings_.slow_test_threshold = self.arguments.slow
        settings_.enable_coverage = self.arguments.enable_coverage

        return settings_

    def create_formatter(self):
        return formatters.DocumentationFormatter(self.create_settings())

    def create_example_collector(self):
        return example_collector.ExampleCollector(self.arguments.specs)

    def create_reporter(self):
        return reporter.Reporter(self.create_formatter())

    def create_runner(self):
        settings = self.create_settings()
        if settings.enable_coverage:
            return runners.CodeCoverageRunner(self.create_example_collector(), self.create_reporter())

        return runners.Runner(self.create_example_collector(), self.create_reporter())

