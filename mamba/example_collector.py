# -*- coding: utf-8 -*-

import os

from mamba import loader

class ExampleCollector(object):

    def __init__(self, paths):
        self.paths = paths

    def collect(self):
        collected = []
        for path in self.paths:
            if not os.path.exists(path):
                continue

            if os.path.isdir(path):
                collected.extend(self._collect_from_directory(path))
            else:
                collected.append(path)
        return collected


    def _collect_from_directory(self, directory):
        collected = []
        for root, dirs, files in os.walk(directory):
            collected.extend([os.path.join(root, file_) for file_ in files if file_.endswith('_spec.py')])

        collected.sort()
        return collected


