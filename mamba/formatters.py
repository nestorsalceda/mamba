# -*- coding: utf-8 -*-

from clint.textui import indent, puts, colored
from mamba import spec


class DocumentationFormatter(object):

    def __init__(self):
        self.has_failed_tests = False
        self.total_specs = 0
        self.total_seconds = .0

    def format(self, item):
        puts(colored.white(item.name))
        self._format_children(item)

    def _format_children(self, item):
        for spec_ in item.specs:
            if isinstance(spec_, spec.Suite):
                self.format_suite(spec_)
            else:
                self.format_spec(spec_)

    def format_suite(self, suite):
        with indent(1 + suite.depth):
            puts(colored.white(suite.name))
            self._format_children(suite)

    def format_spec(self, spec_):
        with indent(1 + spec_.depth):
            symbol = colored.green('✓')
            if spec_.failed:
                symbol = colored.red('✗')
                self.has_failed_tests = True

            puts(symbol + ' ' + spec_.name.replace('_', ' '))

            if spec_.failed:
                with indent(spec_.depth + 2):
                    puts(colored.red(str(spec_.exception_caught())))

        self.total_seconds += spec_.elapsed_time.total_seconds()
        self.total_specs += 1

    def format_summary(self):
        puts()
        color = colored.red if self.has_failed_tests else colored.green
        puts(color("%d specs ran in %.4f seconds" % (self.total_specs, self.total_seconds)))
