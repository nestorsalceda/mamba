# -*- coding: utf-8 -*-

from mamba import settings, formatters, reporter, runners, example_collector, loader
from mamba.infrastructure import is_python3


class ApplicationFactory(object):

    def __init__(self, arguments):
        self._instances = {}
        self.arguments = arguments

    def create_settings(self):
        settings_ = settings.Settings()
        settings_.slow_test_threshold = self.arguments.slow
        settings_.enable_code_coverage = self.arguments.enable_coverage
        settings_.code_coverage_file = self.arguments.coverage_file
        settings_.format = self.arguments.format
        settings_.no_color = self.arguments.no_color
        settings_.match_name = self.arguments.name

        if not is_python3():
            settings_.enable_file_watcher = self.arguments.watch

        return settings_

    def create_formatter(self):
        settings = self.create_settings()
        if settings.format == 'documentation':
            return formatters.DocumentationFormatter(settings)
        return formatters.ProgressFormatter(settings)

    def create_example_collector(self):
        return example_collector.ExampleCollector(self.arguments.specs)

    def create_reporter(self):
        return reporter.Reporter(self.create_formatter())

    def create_runner(self):
        settings = self.create_settings()
        runner = runners.BaseRunner(self.create_example_collector(), loader.Loader(settings.match_name), self.create_reporter())

        if settings.enable_code_coverage:
            runner = runners.CodeCoverageRunner(runner, settings.code_coverage_file)

        if settings.enable_file_watcher:
            runner = runners.FileWatcherRunner(runner)

        return runner
