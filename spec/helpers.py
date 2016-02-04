import ast
import os


def absolute_path_to_fixture_file(root, name):
    return os.path.join(os.path.dirname(root), 'fixtures', name)

def load_ast_of_fixture_file_at(root, name):
    with open(absolute_path_to_fixture_file(root, name)) as fixture_file:
        return ast.parse(fixture_file.read())

def top_level_ast_nodes_of_fixture_at(root, name):
    return load_ast_of_fixture_file_at(root, name).body
