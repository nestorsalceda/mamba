# -*- coding: utf-8 -*-

import traceback

from clint.textui import indent, puts, colored
from mamba import spec


class DocumentationFormatter(object):

    def __init__(self, settings):
        self.settings = settings
        self.total_specs = 0
        self.failed_specs = []
        self.skipped_specs = 0
        self.total_seconds = .0

    @property
    def has_skipped_specs(self):
        return self.skipped_specs != 0

    @property
    def specs_ran(self):
        return self.total_specs - self.skipped_specs

    def format(self, items):
        for item in items:
            self._format_item(item)

            self.total_seconds += item.elapsed_time.total_seconds()

        self.format_summary()

    def _format_item(self, item):
        puts()
        puts(colored.white(item.name))
        self._format_children(item)

    def _format_children(self, item):
        for spec_ in item.specs:
            if isinstance(spec_, spec.SpecGroup):
                self.format_spec_group(spec_)
            else:
                self.format_spec(spec_)

    def format_spec_group(self, spec_group):
        with indent(1 + spec_group.depth):
            if spec_group.skipped:
                puts(colored.yellow(spec_group.name))
            else:
                puts(colored.white(spec_group.name))
            self._format_children(spec_group)

    def format_spec(self, spec_):
        with indent(1 + spec_.depth):
            symbol = colored.green('✓')
            if spec_.failed:
                symbol = colored.red('✗')
                self.failed_specs.append(spec_)
            elif spec_.skipped:
                symbol = colored.yellow('✗')
                self.skipped_specs += 1

            puts(symbol + ' ' + self.format_spec_name(spec_) + self.format_slow_test(spec_))

            if spec_.failed:
                with indent(spec_.depth + 2):
                    puts(colored.red(str(spec_.exception)))

        self.total_specs += 1

    def format_spec_name(self, spec_):
        return spec_.name.replace('_', ' ')

    def format_summary(self):
        puts()
        if self.failed_specs:
            self.format_failed_specs()
            puts(colored.red("%d specs failed of %d ran in %s" % (len(self.failed_specs), self.specs_ran, self.format_seconds(self.total_seconds))))
        elif self.has_skipped_specs:
            puts(colored.yellow("%d specs ran (%d skipped) in %s" % (self.specs_ran, self.skipped_specs, self.format_seconds(self.total_seconds))))
        else:
            puts(colored.green("%d specs ran in %s" % (self.specs_ran, self.format_seconds(self.total_seconds))))

    def format_failed_specs(self):
        puts('Failures:')
        puts()
        with indent(2):
            for index, failed in enumerate(self.failed_specs):
                puts('%d) %s' % (index + 1, self.format_full_spec_name(failed)))
                with indent(3):
                    puts(colored.red('Failure/Error: %s' % self.format_failing_expectation(failed)))
                    puts()
                    puts('Traceback:')
                    puts(colored.red(self.format_traceback(failed)))
                    puts()


    def format_full_spec_name(self, spec_):
        result = [self.format_spec_name(spec_)]

        current = spec_
        while current.parent:
            result.append(self.format_spec_name(current.parent))
            current = current.parent

        result.reverse()
        return ' '.join(result)

    def format_failing_expectation(self, spec_):
        return str(spec_.exception)

    def format_traceback(self, spec_):
        return ''.join([message[2:] for message in traceback.format_tb(spec_.traceback)[1:]])

    def format_seconds(self, seconds):
        return '%.4f seconds' % seconds

    def format_slow_test(self, spec_):
        seconds = spec_.elapsed_time.total_seconds()
        color = None

        if seconds > self.settings.slow_test_threshold:
            color = colored.yellow

            if seconds > 5 * self.settings.slow_test_threshold:
                color = colored.red

        if color is not None:
            return color(' (' + self.format_seconds(seconds) + ')')

        return ''

