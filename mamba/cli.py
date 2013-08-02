# -*- coding: utf-8 -*-

import sys
import os
import argparse

from mamba import formatters, reporter, runner, coverage_collector
from mamba.loader import Loader
from mamba.runner import Runner
from mamba.settings import Settings


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
    settings = _settings_from_arguments(arguments)
    loader = Loader()
    formatter = formatters.DocumentationFormatter(settings)
    reporter_ = reporter.Reporter(formatter)
    runner = Runner(reporter_)

    reporter_.start()
    for file_ in _collect_specs_from(arguments.specs):
        with loader.load_from_file(file_) as module:
            runner.run(getattr(module, 'examples', []))
    reporter_.finish()

    if runner.has_failed_examples:
        sys.exit(1)


def _settings_from_arguments(arguments):
    settings = Settings()
    settings.slow_test_threshold = arguments.slow

    return settings


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
