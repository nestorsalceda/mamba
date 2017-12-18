# -*- coding: utf-8 -*-

import sys
import argparse

from mamba import application_factory, __version__


def main():
    arguments = _parse_arguments()
    if arguments.version:
        print(__version__)
        return

    factory = application_factory.ApplicationFactory(arguments)
    runner = factory.runner()

    runner.run()

    if runner.has_failed_examples:
        sys.exit(1)


def _parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--version', '-v', default=False, action='store_true', help='display the version')
    parser.add_argument('--slow', '-s', default=0.075, type=float, help='slow test threshold in seconds (default: %(default)s)')
    parser.add_argument('--enable-coverage', default=False, action='store_true', help='enable code coverage measurement (default: %(default)s)')
    parser.add_argument('--coverage-file', default='.coverage', action='store', help='name of coverage data file (default: %(default)s)')
    parser.add_argument('--format', '-f', default='progress', action='store', help='output format (default: %(default)s)')
    parser.add_argument('specs', default=['./spec', './specs'], nargs='*', help='paths to specs to run or directories with specs to run (default: %(default)s)')
    parser.add_argument('--no-color', default=False, action='store_true', help='turn off all output coloring (default: %(default)s)')
    parser.add_argument('--tags', '-t', default=None, type=lambda x: [tag.strip() for tag in x.split(',')], action='store', help='run examples with specified tags (example: -t unit,integration)')

    return parser.parse_args()


if __name__ == '__main__':
    main()
