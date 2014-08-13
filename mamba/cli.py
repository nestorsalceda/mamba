# -*- coding: utf-8 -*-

import sys
import argparse

from mamba import application_factory, __version__
from mamba.infrastructure import is_python3


def main():
    arguments = _parse_arguments()
    if arguments.version:
        print(__version__)
        return

    factory = application_factory.ApplicationFactory(arguments)
    runner = factory.create_runner()

    runner.run()

    if runner.has_failed_examples:
        sys.exit(1)


def _parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--version', '-v', default=False, action='store_true', help='Display the version.')
    parser.add_argument('--slow', '-s', default=0.075, type=float, help='Slow test threshold in seconds (default: %(default)s)')
    parser.add_argument('--enable-coverage', default=False, action='store_true', help='Enable code coverage measurement (default: %(default)s)')
    parser.add_argument('--format', '-f', default='documentation', action='store', choices=['documentation', 'progress'], help='Output format (default: %(default)s)')
    parser.add_argument('specs', default=['spec', 'specs'], nargs='*', help='Specs or directories with specs to run (default: %(default)s)')
    parser.add_argument('--no-color', default=False, action='store_true', help='Turn off all output coloring (default: %(default)s)')

    if not is_python3():
        parser.add_argument('--watch', '-w', default=False, action='store_true', help='Enable file watching support - not available with python3 (default: %(default)s)')

    return parser.parse_args()


if __name__ == '__main__':
    main()
