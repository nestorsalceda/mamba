# -*- coding: utf-8 -*-

from mamba import loader


class Runner(object):

    def __init__(self, example_collector, reporter):
        self.reporter = reporter
        self.has_failed_examples = False
        self.example_collector = example_collector
        self._loader = loader.Loader()

    def run(self):
        self.reporter.start()
        for file_ in self.example_collector.collect():
            with self._loader.load_from_file(file_) as module:
                self._run_examples_in(module)
        self.reporter.finish()

    def _run_examples_in(self, module):
        for example in getattr(module, 'examples', []):
            example.run(self.reporter)

            if example.failed:
                self.has_failed_examples = True
