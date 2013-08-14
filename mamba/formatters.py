# -*- coding: utf-8 -*-

import traceback

from clint.textui import indent, puts, colored

from mamba.example_group import PendingExampleGroup


class Formatter(object):

    def example_started(self, example):
        pass

    def example_passed(self, example):
        pass

    def example_failed(self, example):
        pass

    def example_pending(self, example):
        pass

    def example_group_started(self, example_group):
        pass

    def example_group_finished(self, example_group):
        pass

    def example_group_pending(self, example_group):
        pass

    def summary(self, duration, example_count, failed_count, pending_count):
        pass

    def failures(self, failed_examples):
        pass


class DocumentationFormatter(Formatter):

    def __init__(self, settings):
        self.settings = settings

    def example_passed(self, example):
        self._format_example(colored.green('✓'), example)

    def example_failed(self, example):
        self._format_example(colored.red('✗'), example)
        with indent((self._depth(example) + 1) * 2):
            puts(colored.red(str(example.error.exception)))

    def _depth(self, example):
        depth = 0
        current = example.parent
        while current is not None:
            depth += 1
            current = current.parent

        return depth

    def example_pending(self, example):
        self._format_example(colored.yellow('✗'), example)

    def _format_example(self, symbol, example):
        puts('  ' * self._depth(example) + symbol + ' ' + self._format_example_name(example) + self._format_slow_test(example))

    def _format_example_name(self, example):
        return example.name.replace('_', ' ')

    def _format_slow_test(self, example):
        seconds = example.elapsed_time.total_seconds()
        color = None

        if seconds > self.settings.slow_test_threshold:
            color = colored.yellow

            if seconds > 5 * self.settings.slow_test_threshold:
                color = colored.red

        if color is not None:
            return color(' (' + self._format_duration(example.elapsed_time) + ')')

        return ''

    def example_group_started(self, example_group):
        self._format_example_group(example_group, colored.white)

    def example_group_finished(self, example_group):
        if example_group.parent is None:
            puts()

    def example_group_pending(self, example_group):
        self._format_example_group(example_group, colored.yellow)

    def _format_example_group(self, example_group, color):
        puts('  ' * self._depth(example_group) + color(example_group.name))

    def summary(self, duration, example_count, failed_count, pending_count):
        duration = self._format_duration(duration)
        if failed_count != 0:
            puts(colored.red("%d examples failed of %d ran in %s" % (failed_count, example_count, duration)))
        elif pending_count != 0:
            puts(colored.yellow("%d examples ran (%d pending) in %s" % (example_count, pending_count, duration)))
        else:
            puts(colored.green("%d examples ran in %s" % (example_count, duration)))

    def _format_duration(self, duration):
        return '%.4f seconds' % duration.total_seconds()

    def failures(self, failed_examples):
        if not failed_examples:
            return

        puts()
        puts('Failures:')
        puts()
        with indent(2):
            for index, failed in enumerate(failed_examples):
                puts('%d) %s' % (index + 1, self._format_full_example_name(failed)))
                with indent(3):
                    puts(colored.red('Failure/Error: %s' % self._format_failing_expectation(failed)))
                    puts()
                    puts('Traceback:')
                    puts(colored.red(self._format_traceback(failed)))
                    puts()


    def _format_full_example_name(self, example):
        result = [self._format_example_name(example)]

        current = example
        while current.parent:
            result.append(self._format_example_name(current.parent))
            current = current.parent

        result.reverse()
        return ' '.join(result)

    def _format_failing_expectation(self, example_):
        return str(example_.error.exception)

    def _format_traceback(self, example_):
        return ''.join([message[2:] for message in traceback.format_tb(example_.error.traceback)[1:]])

