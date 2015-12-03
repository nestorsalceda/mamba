# -*- coding: utf-8 -*-

from mamba import formatters, reporter, runners, example_collector, loader
from mamba.settings import Settings
from mamba.infrastructure import is_python3


class ApplicationFactory(object):

    def __init__(self, arguments):
        self._arguments = arguments

    def create_settings(self):
        settings = Settings()
        settings.slow_test_threshold = self._arguments.slow
        settings.enable_code_coverage = self._arguments.enable_coverage
        settings.format = self._arguments.format
        settings.no_color = self._arguments.no_color

        if not is_python3():
            settings.enable_file_watcher = self._arguments.watch

        return settings

    def create_formatter(self):
        settings = self.create_settings()
        if settings.format == 'documentation':
            return formatters.DocumentationFormatter(settings)
        return formatters.ProgressFormatter(settings)

    def create_example_collector(self):
        return example_collector.ExampleCollector(self._arguments.specs)

    def create_reporter(self):
        return reporter.Reporter(self.create_formatter())

    def create_runner(self):
        settings = self.create_settings()
        runner = runners.BaseRunner(self.create_example_collector(), loader.Loader(), self.create_reporter())

        if settings.enable_code_coverage:
            runner = runners.CodeCoverageRunner(runner)

        if settings.enable_file_watcher:
            runner = runners.FileWatcherRunner(runner)

        return runner
