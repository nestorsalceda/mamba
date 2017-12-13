# -*- coding: utf-8 -*-

from mamba import runnable
from mamba.infrastructure import code_coverage


class Runner(object):

    def run(self):
        raise NotImplementedError()

    @property
    def has_failed_examples(self):
        raise NotImplementedError()


class BaseRunner(Runner):

    def __init__(self, example_collector, loader, reporter, tags):
        self.example_collector = example_collector
        self.loader = loader
        self.reporter = reporter
        self._has_failed_examples = False
        self.tags = tags

    def run(self):
        self.reporter.start()

        modules = self.example_collector.modules()

        if self._any_module_has_focused_examples(modules):
            self.tags = ['focus']

        for module in modules:
            self._run_examples_in(module)

        self.reporter.finish()

    def _any_module_has_focused_examples(self, modules):
        return any(getattr(module, '__mamba_has_focused_examples') for module in modules)

    def _run_examples_in(self, module):
        for example in self.loader.load_examples_from(module):
            example.execute(self.reporter,
                            runnable.ExecutionContext(),
                            tags=self.tags)

            if example.failed():
                self._has_failed_examples = True

    @property
    def has_failed_examples(self):
        return self._has_failed_examples


class CodeCoverageRunner(Runner):

    def __init__(self, runner, code_coverage_file):
        self.runner = runner
        self.code_coverage_file = code_coverage_file

    def run(self):
        with code_coverage.CodeCoverage(self.code_coverage_file):
            self.runner.run()

    @property
    def has_failed_examples(self):
        return self.runner.has_failed_examples
