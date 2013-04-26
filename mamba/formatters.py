# -*- coding: utf-8 -*-

from clint.textui import indent, puts, colored
from mamba import spec


class DocumentationFormatter(object):

    def __init__(self):
        self.total_specs = 0
        self.failed_specs = 0
        self.skipped_specs = 0
        self.total_seconds = .0

    @property
    def has_failed_specs(self):
        return self.failed_specs != 0

    @property
    def has_skipped_specs(self):
        return self.skipped_specs != 0

    @property
    def specs_ran(self):
        return self.total_specs - self.skipped_specs

    def format(self, item):
        puts()
        puts(colored.white(item.name))
        self._format_children(item)

        self.total_seconds += item.elapsed_time.total_seconds()

    def _format_children(self, item):
        for spec_ in item.specs:
            if isinstance(spec_, spec.Suite):
                self.format_suite(spec_)
            else:
                self.format_spec(spec_)

    def format_suite(self, suite):
        with indent(1 + suite.depth):
            if suite.skipped:
                puts(colored.yellow(suite.name))
            else:
                puts(colored.white(suite.name))
            self._format_children(suite)

    def format_spec(self, spec_):
        with indent(1 + spec_.depth):
            symbol = colored.green('✓')
            if spec_.failed:
                symbol = colored.red('✗')
                self.failed_specs += 1
            elif spec_.skipped:
                symbol = colored.yellow('✗')
                self.skipped_specs += 1

            puts(symbol + ' ' + spec_.name.replace('_', ' '))

            if spec_.failed:
                with indent(spec_.depth + 2):
                    puts(colored.red(str(spec_.exception_caught())))

        self.total_specs += 1

    def format_summary(self):
        puts()
        if self.has_failed_specs:
            puts(colored.red("%d specs failed of %d ran in %.4f seconds" % (self.failed_specs, self.specs_ran, self.total_seconds)))
        elif self.has_skipped_specs:
            puts(colored.yellow("%d specs ran (%d skipped) in %.4f seconds" % (self.specs_ran, self.skipped_specs, self.total_seconds)))
        else:
            puts(colored.green("%d specs ran in %.4f seconds" % (self.specs_ran, self.total_seconds)))
