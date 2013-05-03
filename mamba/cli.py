# -*- coding: utf-8 -*-

import sys
import os
import imp
import argparse

from mamba import formatters
from mamba.runner import Runner
from mamba.settings import Settings


def main():
    arguments = _parse_arguments()
    settings = _settings_from_arguments(arguments)
    formatter = formatters.DocumentationFormatter(settings)
    runner = Runner(formatter)

    for file_ in _collect_specs_from(arguments.specs):
        module = imp.load_source(file_.replace('.py', ''), file_)
        runner.run(module)

    formatter.format_summary()

    if runner.has_failed_specs:
        sys.exit(1)

def _parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--slow', '-s', default=0.075, type=float, help='slow test threshold in seconds (default: %(default)s)')
    parser.add_argument('specs', default=['spec'], nargs='*', help='specs or directories with specs to run (default: %(default)s)')

    args = parser.parse_args()
    return args


def _settings_from_arguments(arguments):
    settings = Settings()
    settings.slow_test_threshold = arguments.slow

    return settings


def _collect_specs_from(specs):
    collected = []
    for path in specs:
        if os.path.isdir(path):
            collected.extend(_collect_specs_from_directory(path))
        else:
            collected.append(path)
    return collected


def _collect_specs_from_directory(directory):
    collected = []
    for root, dirs, files in os.walk(directory):
        collected.extend([os.path.join(root, file_) for file_ in files if file_.endswith('_spec.py')])

    collected.sort()
    return collected


if __name__ == '__main__':
    main()
