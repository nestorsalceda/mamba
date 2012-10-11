# -*- coding: utf-8 -*-

import sys
import imp

from clint.textui import indent, puts, colored

from mamba.runner import Runner
from mamba.spec import Suite

_total_seconds = 0.0
_total_specs = 0


def main():
    runner = Runner()

    for file_ in sys.argv[1:]:
        module = imp.load_source(file_.replace('.py', ''), file_)
        runner.run(module)

        for spec in module.specs:
            if isinstance(spec, Suite):
                _format_suite(spec)
            else:
                _format_spec(spec)

    puts()
    puts("%d specs ran in %.4f seconds" % (_total_specs, _total_seconds))


def _format_suite(suite):
    with indent(1 + suite.depth()):
        puts(colored.white(suite.name()))

        for spec in suite.specs:
            if isinstance(spec, Suite):
                _format_suite(spec)
            else:
                _format_spec(spec)


def _format_spec(spec):
    with indent(1 + spec.depth()):
        symbol = colored.green('✓')
        if spec.exception_caught() is not None:
            symbol = colored.red('✗')

        puts(symbol + ' ' + spec.name().replace('_', ' '))

        if spec.exception_caught() is not None:
            with indent(spec.depth() + 2):
                puts(colored.red(str(spec.exception_caught())))

        global _total_seconds
        global _total_specs

        _total_seconds += spec.elapsed_time().total_seconds()
        _total_specs += 1

if __name__ == '__main__':
    main()
