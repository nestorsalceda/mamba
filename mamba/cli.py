# -*- coding: utf-8 -*-

import sys
import os
import imp

from mamba import formatters
from mamba.runner import Runner


def main():
    formatter = formatters.DocumentationFormatter()
    runner = Runner(formatter)

    for file_ in _collect_specs_from_argv():
        module = imp.load_source(file_.replace('.py', ''), file_)
        runner.run(module)

    formatter.format_summary()

    if runner.has_failed_specs:
        sys.exit(1)


def _collect_specs_from_argv():
    if len(sys.argv) == 1:
        return _collect_specs_from_directory('spec')

    collected = []
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            collected.extend(_collect_specs_from_directory(arg))
        else:
            collected.append(arg)
    return collected


def _collect_specs_from_directory(directory):
    collected = []
    for root, dirs, files in os.walk(directory):
        collected.extend([os.path.join(root, file_) for file_ in files if file_.endswith('_spec.py')])

    collected.sort()
    return collected

if __name__ == '__main__':
    main()
