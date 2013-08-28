# -*- coding: utf-8 -*-

import os

from mamba import loader

class ExampleCollector(object):

    def __init__(self, paths):
        self.paths = paths
        self._loader = loader.Loader()

    def modules(self):
        for file_ in self._collect_files_containing_examples():
            with self._loader.load_from_file(file_) as module:
                if self._has_examples(module):
                    yield module

    def _collect_files_containing_examples(self):
        collected = []
        for path in self.paths:
            if not os.path.exists(path):
                continue

            if os.path.isdir(path):
                collected.extend(self._collect_files_in_directory(path))
            else:
                collected.append(path)
        return collected


    def _collect_files_in_directory(self, directory):
        collected = []
        for root, dirs, files in os.walk(directory):
            collected.extend([os.path.join(root, file_) for file_ in files if file_.endswith('_spec.py')])

        collected.sort()
        return collected

    def _has_examples(self, module):
        return hasattr(module, 'examples')

