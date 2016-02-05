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
        return [
            self._load_module_from(path)
            for path in self._collect_paths_to_spec_files()
        ]

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
        for root, file_names in self._walk_directory_from_top_to_bottom(path_to_directory):
            paths_to_spec_files.extend([
                self._assemble_path_to_spec_file(root, file_name)
                for file_name in file_names if self._is_name_of_spec_file(file_name)
            ])

        paths_to_spec_files.sort()

        return paths_to_spec_files

    def _walk_directory_from_top_to_bottom(self, path_to_directory):
        for root, _, file_names in os.walk(path_to_directory):
            yield (root, file_names)

    def _assemble_path_to_spec_file(self, path_to_directory, name_of_spec_file):
        return os.path.join(self._normalize_path(path_to_directory), name_of_spec_file)

    def _normalize_path(self, path):
        return os.path.normpath(path)

    def _is_name_of_spec_file(self, file_name):
        return file_name.endswith(ExampleCollector.SPEC_FILE_NAME_ENDING)

    #TODO: What about managing locks with threads??
    #Take care with watchdog stuff!!
    def _load_module_from(self, path_to_spec_file):
        module_name = self._dump_file_extension(path_to_spec_file)

        return self._module_from_ast(module_name, path_to_spec_file)

    def _dump_file_extension(self, path_to_file):
        return os.path.splitext(path_to_file)[0]

    def _module_from_ast(self, module_name, path_to_spec_file):
        module = self._create_module_object(module_name, path_to_spec_file)
        code_object_of_transformed_ast = self._create_code_object_from_ast(
            self._transform_ast_of_source_code_at(path_to_spec_file),
            path_to_spec_file
        )

        with self._allow_importing_local_non_installed_modules():
            self._execute_code_object_in_namespace(code_object_of_transformed_ast, module.__dict__)

        return module

    def _create_module_object(self, name, path_to_code_of_module):
        module = imp.new_module(name)
        module.__file__ = path_to_code_of_module
        self._import_package_of_module(module)

        return module

    def _import_package_of_module(self, module):
        package_name = '.'.join(module.__name__.split('/')[:-1])

        try:
            __import__(package_name)
        except (ImportError, ValueError):
            # No parent package available, so skip it
            pass
        else:
            module.__package__ = package_name

    def _transform_ast_of_source_code_at(self, path_to_spec_file):
        original_source_code = self._read_contents_of_file_at(path_to_spec_file)
        ast_of_original_source_code = self._get_ast_of(original_source_code, path_to_spec_file)

        return self._transform_ast(ast_of_original_source_code)

    def _read_contents_of_file_at(self, path):
        with open(path) as file_:
            return file_.read()

    def _get_ast_of(self, source, file_name):
        return ast.parse(source, filename=file_name)

    def _transform_ast(self, an_ast):
        transformed_ast = self._node_transformer.visit(an_ast)
        ast.fix_missing_locations(transformed_ast)

        return transformed_ast

    def _create_code_object_from_ast(self, ast, path_to_spec_file):
        return compile(ast, path_to_spec_file, 'exec')

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

    def _execute_code_object_in_namespace(self, code_object, namespace):
        exec(code_object, namespace)
