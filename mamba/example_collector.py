# -*- coding: utf-8 -*-

import os
import sys
import imp
import ast
import contextlib

from .syntax.transformer import MambaSyntaxToClassBasedSyntax


class ExampleCollector(object):

    def __init__(self, paths):
        self.paths = paths
        self._ast_transformer = MambaSyntaxToClassBasedSyntax()

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

    #TODO: What about managing locks with threads??
    #Take care with watchdog stuff!!
    @contextlib.contextmanager
    def _load_module_from(self, path):
        name = path.replace('.py', '')

        yield self._module_from_ast(name, path)

    def _module_from_ast(self, name, path):
        tree = self._parse_and_transform_ast(path)
        package = '.'.join(name.split('/')[:-1])

        module = imp.new_module(name)
        module.__file__ = path

        try:
            __import__(package)
            module.__package__ = package
        except (ImportError, ValueError):
            # No parent package available, so skip it
            pass

        self._prepare_path_for_local_packages()
        code = compile(tree, path, 'exec')
        exec(code, module.__dict__)
        self._restore_path()

        return module

    def _parse_and_transform_ast(self, path):
        with open(path) as f:
            tree = ast.parse(f.read(), filename=path)

        return self._ast_transformer.transform(tree)

    def _prepare_path_for_local_packages(self):
        if os.getcwd().endswith('spec') or os.getcwd().endswith('specs'):
            sys.path.append('..')
        else:
            sys.path.append('.')

    def _restore_path(self):
        sys.path.pop()
