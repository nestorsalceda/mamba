# -*- coding: utf-8 -*-

import traceback

from clint.textui import indent, puts, colored


class Formatter(object):

    def spec_started(self, spec):
        pass

    def spec_passed(self, spec):
        pass

    def spec_failed(self, spec):
        pass

    def spec_pending(self, spec):
        pass

    def spec_group_started(self, spec_group):
        pass

    def spec_group_finished(self, spec_group):
        pass

    def summary(self, duration, spec_count, failed_count, pending_count):
        pass

    def failures(self, failed_specs):
        pass


class DocumentationFormatter(Formatter):

    def __init__(self, settings):
        self.settings = settings

    def spec_passed(self, spec):
        self._format_spec(colored.green('✓'), spec)

    def spec_failed(self, spec):
        self._format_spec(colored.red('✗'), spec)
        with indent((spec.depth + 1) * 2):
            puts(colored.red(str(spec.exception)))

    def spec_pending(self, spec):
        self._format_spec(colored.yellow('✗'), spec)

    def _format_spec(self, symbol, spec):
        puts('  ' * spec.depth + symbol + ' ' + self._format_spec_name(spec) + self._format_slow_test(spec))

    def _format_spec_name(self, spec):
        return spec.name.replace('_', ' ')

    def _format_slow_test(self, spec):
        seconds = spec.elapsed_time.total_seconds()
        color = None

        if seconds > self.settings.slow_test_threshold:
            color = colored.yellow

            if seconds > 5 * self.settings.slow_test_threshold:
                color = colored.red

        if color is not None:
            return color(' (' + self._format_duration(spec.elapsed_time) + ')')

        return ''

    def spec_group_started(self, spec_group):
        if spec_group.pending:
            puts('  ' * spec_group.depth + colored.yellow(spec_group.name))
        else:
            puts('  ' * spec_group.depth + colored.white(spec_group.name))

    def spec_group_finished(self, spec_group):
        if spec_group.depth == 0:
            puts()

    def summary(self, duration, spec_count, failed_count, pending_count):
        duration = self._format_duration(duration)
        if failed_count != 0:
            puts(colored.red("%d specs failed of %d ran in %s" % (failed_count, spec_count, duration)))
        elif pending_count != 0:
            puts(colored.yellow("%d specs ran (%d pending) in %s" % (spec_count, pending_count, duration)))
        else:
            puts(colored.green("%d specs ran in %s" % (spec_count, duration)))

    def _format_duration(self, duration):
        return '%.4f seconds' % duration.total_seconds()

    def failures(self, failed_specs):
        if not failed_specs:
            return

        puts()
        puts('Failures:')
        puts()
        with indent(2):
            for index, failed in enumerate(failed_specs):
                puts('%d) %s' % (index + 1, self._format_full_spec_name(failed)))
                with indent(3):
                    puts(colored.red('Failure/Error: %s' % self._format_failing_expectation(failed)))
                    puts()
                    puts('Traceback:')
                    puts(colored.red(self._format_traceback(failed)))
                    puts()


    def _format_full_spec_name(self, spec):
        result = [self._format_spec_name(spec)]

        current = spec
        while current.parent:
            result.append(self._format_spec_name(current.parent))
            current = current.parent

        result.reverse()
        return ' '.join(result)

    def _format_failing_expectation(self, spec_):
        return str(spec_.exception)

    def _format_traceback(self, spec_):
        return ''.join([message[2:] for message in traceback.format_tb(spec_.traceback)[1:]])

