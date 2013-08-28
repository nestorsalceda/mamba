# -*- coding: utf-8 -*-

import sys
import os
import argparse

from mamba import coverage_collector, application_factory


def main():
    arguments = _parse_arguments()
    if arguments.disable_coverage:
        _run_without_coverage(arguments)
    else:
        _run_with_coverage(arguments)


def _parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--slow', '-s', default=0.075, type=float, help='slow test threshold in seconds (default: %(default)s)')
    parser.add_argument('--disable-coverage', default=False, action='store_true', help='disable coverage measurement (default: %(default)s)')
    parser.add_argument('specs', default=['spec'], nargs='*', help='specs or directories with specs to run (default: %(default)s)')

    args = parser.parse_args()
    return args


def _run_without_coverage(arguments):
    _run(arguments)


def _run_with_coverage(arguments):
    with coverage_collector.CoverageCollector():
        _run(arguments)


def _run(arguments):
    factory = application_factory.ApplicationFactory(arguments)
    runner = factory.create_runner()

    runner.run(_collect_specs_from(arguments.specs))

    if runner.has_failed_examples:
        sys.exit(1)


def _collect_specs_from(specs):
    collected = []
    for path in specs:
        if not os.path.exists(path):
            continue

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
