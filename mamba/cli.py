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

    runner.run()

    if runner.has_failed_examples:
        sys.exit(1)


if __name__ == '__main__':
    main()
