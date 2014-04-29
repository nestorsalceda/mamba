# -*- coding: utf-8 -*-

import os
import sys
import imp
import ast
import contextlib

from mamba import nodetransformers

class ExampleCollector(object):

    def __init__(self, paths):
        self.paths = paths

    def modules(self):
        for path in self._collect_files_containing_examples():
            with self._load_module_from(path) as module:
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
            collected.extend([os.path.join(self._normalize_path(root), file_)
                    for file_ in files if file_.endswith('_spec.py')])
        collected.sort()
        return collected

    def _normalize_path(self, path):
        return os.path.normpath(path)

    @contextlib.contextmanager
    def _load_module_from(self, path):
        with open(path) as f:
            tree = ast.parse(f.read(), filename=path)
            tree = nodetransformers.TransformToSpecsNodeTransformer().visit(tree)
            ast.fix_missing_locations(tree)

        name = path.replace('.py', '')

        module = imp.new_module(name)
        module.__package__ = name.rpartition('.')[0]
        module.__file__ = path

        code = compile(tree, path, 'exec')
        exec(code, module.__dict__)

        yield module

    @contextlib.contextmanager
    def _path(self, path):
        old_path = list(sys.path)

        sys.path.append(path)

        try:
            yield
        finally:
            sys.path = old_path

    def _split_into_module_path_and_name(self, path):
        dirname, basename = os.path.split(path)

        module_path = basename
        package_path = None

        while dirname:
            if os.path.exists(os.path.join(dirname, '__init__.py')):
                package_path = dirname
            elif package_path is not None:
                break

            dirname, basename = os.path.split(dirname)

            module_path = os.path.join(basename, module_path)

        return dirname, module_path.replace('.py', '').replace(os.sep, '.')


