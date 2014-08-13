# -*- coding: utf-8 -*-

from mamba.infrastructure import code_coverage, file_watcher


class Runner(object):

    def run(self):
        raise NotImplementedError()

    @property
    def has_failed_examples(self):
        raise NotImplementedError()


class BaseRunner(Runner):

    def __init__(self, example_collector, loader, reporter):
        self.example_collector = example_collector
        self.loader = loader
        self.reporter = reporter
        self._has_failed_examples = False

    def run(self):
        self.reporter.start()

        for module in self.example_collector.modules():
            self._run_examples_in(module)

        self.reporter.finish()

    def _run_examples_in(self, module):
        for example in self.loader.load_examples_from(module):
            example.run(self.reporter)

            if example.failed:
                self._has_failed_examples = True

    @property
    def has_failed_examples(self):
        return self._has_failed_examples


class CodeCoverageRunner(Runner):

    def __init__(self, runner):
        self.runner = runner

    def run(self):
        with code_coverage.CodeCoverage():
            self.runner.run()

    @property
    def has_failed_examples(self):
        return self.runner.has_failed_examples


class FileWatcherRunner(Runner):

    def __init__(self, runner):
        self.file_watcher = file_watcher.FileWatcher(runner)

    def run(self):
        self.file_watcher.wait_for_events()

    @property
    def has_failed_examples(self):
        return False
