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
    def _load_module_from(self, path_to_spec_file):
        module_name = self._dump_file_extension(path_to_spec_file)

        yield self._module_from_ast(module_name, path_to_spec_file)

    def _dump_file_extension(self, path_to_file):
        return os.path.splitext(path_to_file)[0]

    def _module_from_ast(self, module_name, path_to_spec_file):
        tree = self._parse_and_transform_ast(path_to_spec_file)
        module = self._create_module_object(module_name, path_to_spec_file)

        with self._allow_importing_local_non_installed_modules():
            code = compile(tree, path_to_spec_file, 'exec')
            exec(code, module.__dict__)

        return module

    def _create_module_object(self, module_name, path_to_spec_file):
        package_name = '.'.join(module_name.split('/')[:-1])

        module = imp.new_module(module_name)
        module.__file__ = path_to_spec_file

        try:
            __import__(package_name)
        except (ImportError, ValueError):
            # No parent package available, so skip it
            pass
        else:
            module.__package__ = package_name

        return module

    def _parse_and_transform_ast(self, path_to_spec_file):
        with open(path_to_spec_file) as spec_file:
            tree = ast.parse(spec_file.read(), filename=path_to_spec_file)
            tree = self._node_transformer.visit(tree)
            ast.fix_missing_locations(tree)
            return tree

    @contextlib.contextmanager
    def _allow_importing_local_non_installed_modules(self):
        self._append_parent_directory_of_spec_directory_to_system_path()
        yield
        self._remove_last_item_from_system_path()

    def _append_parent_directory_of_spec_directory_to_system_path(self):
        if os.getcwd().endswith('spec') or os.getcwd().endswith('specs'):
            sys.path.append('..')
        else:
            sys.path.append('.')

    def _remove_last_item_from_system_path(self):
        sys.path.pop()
