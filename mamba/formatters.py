# -*- coding: utf-8 -*-

from clint.textui import indent, puts, colored
from mamba import spec


class DocumentationFormatter(object):

    def __init__(self, settings):
        self.settings = settings
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
                self.failed_specs += 1
            elif spec_.skipped:
                symbol = colored.yellow('✗')
                self.skipped_specs += 1

            puts(symbol + ' ' + spec_.name.replace('_', ' ') + self.format_slow_test(spec_))

            if spec_.failed:
                with indent(spec_.depth + 2):
                    puts(colored.red(str(spec_.exception)))

        self.total_specs += 1

    def format_summary(self):
        puts()
        if self.has_failed_specs:
            puts(colored.red("%d specs failed of %d ran in %s" % (self.failed_specs, self.specs_ran, self.format_seconds(self.total_seconds))))
        elif self.has_skipped_specs:
            puts(colored.yellow("%d specs ran (%d skipped) in %s" % (self.specs_ran, self.skipped_specs, self.format_seconds(self.total_seconds))))
        else:
            puts(colored.green("%d specs ran in %s" % (self.specs_ran, self.format_seconds(self.total_seconds))))

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

