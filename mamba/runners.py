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
        self._example_collector = example_collector
        self._loader = loader
        self._reporter = reporter
        self._has_failed_examples = False

    def run(self):
        self._reporter.start()

        for module in self._example_collector.modules():
            self._run_examples_in(module)

        self._reporter.finish()

    def _run_examples_in(self, module):
        for example_group in self._loader.load_examples_from(module):
            example_group.run(self._reporter)

            if example_group.failed:
                self._has_failed_examples = True

    @property
    def has_failed_examples(self):
        return self._has_failed_examples


class CodeCoverageRunner(Runner):

    def __init__(self, runner):
        self._runner = runner

    def run(self):
        with code_coverage.CodeCoverage():
            self._runner.run()

    @property
    def has_failed_examples(self):
        return self._runner.has_failed_examples


class FileWatcherRunner(Runner):

    def __init__(self, runner):
        self._file_watcher = file_watcher.FileWatcher(runner)

    def run(self):
        self._file_watcher.wait_for_events()

    @property
    def has_failed_examples(self):
        return False
