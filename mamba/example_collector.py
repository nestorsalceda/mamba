# -*- coding: utf-8 -*-

import os
import sys
import imp
import ast
import contextlib

from mamba import nodetransformers
from mamba.infrastructure import is_python3

class ExampleCollector(object):
    SPEC_FILE_NAME_ENDING = '_spec.py'

    def __init__(self, paths_to_spec_directories_or_files):
        self.paths_to_specs = paths_to_spec_directories_or_files
        self._node_transformer = nodetransformers.TransformToSpecsPython3NodeTransformer() if is_python3() else nodetransformers.TransformToSpecsNodeTransformer()

    def modules(self):
        for path_to_spec_file in self._collect_paths_to_spec_files():
            with self._load_module_from(path_to_spec_file) as module:
                yield module

    def _collect_paths_to_spec_files(self):
        paths_to_spec_files = []
        for path in self.paths_to_specs:
            if not os.path.exists(path):
                continue

            if os.path.isdir(path):
                paths_to_spec_files.extend(self._collect_paths_to_spec_files_in_directory(path))
            else:
                paths_to_spec_files.append(path)

        return paths_to_spec_files

    def _collect_paths_to_spec_files_in_directory(self, path_to_directory):
        paths_to_spec_files = []
        for root, _, file_names in os.walk(path_to_directory):
            paths_to_spec_files.extend([
                self._assemble_path_to_spec_file(root, file_name)
                for file_name in file_names if self._is_name_of_spec_file(file_name)
            ])

        paths_to_spec_files.sort()

        return paths_to_spec_files

    def _assemble_path_to_spec_file(self, path_to_directory, name_of_spec_file):
        return os.path.join(self._normalize_path(path_to_directory), name_of_spec_file)

    def _normalize_path(self, path):
        return os.path.normpath(path)

    def _is_name_of_spec_file(self, file_name):
        return file_name.endswith(ExampleCollector.SPEC_FILE_NAME_ENDING)

    #TODO: What about managing locks with threads??
    #Take care with watchdog stuff!!
    @contextlib.contextmanager
    def _load_module_from(self, path):
        module_name = self._dump_file_extension(path)

        yield self._module_from_ast(module_name, path)

    def _dump_file_extension(self, path_to_file):
        return os.path.splitext(path_to_file)[0]

    def _module_from_ast(self, module_name, path):
        tree = self._parse_and_transform_ast(path)
        package = '.'.join(module_name.split('/')[:-1])

        module = imp.new_module(module_name)
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
            tree = self._node_transformer.visit(tree)
            ast.fix_missing_locations(tree)
            return tree

    def _prepare_path_for_local_packages(self):
        if os.getcwd().endswith('spec') or os.getcwd().endswith('specs'):
            sys.path.append('..')
        else:
            sys.path.append('.')

    def _restore_path(self):
        sys.path.pop()
