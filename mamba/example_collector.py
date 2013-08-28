# -*- coding: utf-8 -*-

import os
import sys
import imp
import contextlib

class ExampleCollector(object):

    def __init__(self, paths):
        self.paths = paths

    def modules(self):
        for path in self._collect_files_containing_examples():
            with self._load_module_from(path) as module:
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

    @contextlib.contextmanager
    def _load_module_from(self, path):
        name = path.replace('.py', '')
        try:
            yield imp.load_source(name, path)
        finally:
            if name in sys.modules:
                del sys.modules[name]

    def _has_examples(self, module):
        return hasattr(module, 'examples')

