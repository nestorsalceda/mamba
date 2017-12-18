# -*- coding: utf-8 -*-

from importlib import import_module

from mamba import settings, formatters, reporter, runners, example_collector, loader


class ApplicationFactory(object):

    def __init__(self, arguments):
        self._instances = {}
        self.arguments = arguments
        self.settings = self._settings(self.arguments)

    def _settings(self, arguments):
        settings_ = settings.Settings()
        settings_.slow_test_threshold = self.arguments.slow
        settings_.enable_code_coverage = self.arguments.enable_coverage
        settings_.code_coverage_file = self.arguments.coverage_file
        settings_.format = self.arguments.format
        settings_.no_color = self.arguments.no_color
        settings_.tags = self.arguments.tags

        return settings_

    def runner(self):
        runner = runners.BaseRunner(self._example_collector(),
                                    self._loader(),
                                    self._reporter(),
                                    self.settings.tags)

        if self.settings.enable_code_coverage:
            runner = runners.CodeCoverageRunner(runner,
                                                self.settings.code_coverage_file)

        return runner

    def _example_collector(self):
        return example_collector.ExampleCollector(self.arguments.specs)

    def _loader(self):
        return loader.Loader()

    def _reporter(self):
        return reporter.Reporter(self._formatter())

    def _formatter(self):
        if self.settings.format == 'progress':
            return formatters.ProgressFormatter(self.settings)
        if self.settings.format == 'documentation':
            return formatters.DocumentationFormatter(self.settings)

        return self._custom_formatter()

    def _custom_formatter(self):
        splitted = self.settings.format.split('.')
        module = import_module('.'.join(splitted[0:-1]), splitted[-1])
        formatter = getattr(module, splitted[-1])

        return formatter(self.settings)
