# -*- coding: utf-8 -*-

from mamba import settings, formatters, reporter, runner, example_collector


class ApplicationFactory(object):

    def __init__(self, arguments):
        self._instances = {}
        self.arguments = arguments

    def create_settings(self):
        settings_ = settings.Settings()
        settings_.slow_test_threshold = self.arguments.slow

        return settings_

    def create_formatter(self):
        return formatters.DocumentationFormatter(self.create_settings())

    def create_example_collector(self):
        return example_collector.ExampleCollector(self.arguments.specs)

    def create_reporter(self):
        return reporter.Reporter(self.create_formatter())

    def create_runner(self):
        return runner.Runner(self.create_example_collector(), self.create_reporter())

