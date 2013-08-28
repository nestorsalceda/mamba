# -*- coding: utf-8 -*-

from mamba import loader


class Runner(object):

    def __init__(self, reporter):
        self.reporter = reporter
        self.has_failed_examples = False
        self.loader = loader.Loader()

    def run(self, files):
        self.reporter.start()
        for file_ in files:
            with self.loader.load_from_file(file_) as module:
                self._run_spec(module)
        self.reporter.finish()

    def _run_spec(self, module):
        for example in getattr(module, 'examples', []):
            example.run(self.reporter)

            if example.failed:
                self.has_failed_examples = True
