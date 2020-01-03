# -*- coding: utf-8 -*-

import sys
import traceback
import inspect

from clint.textui import indent, puts, colored


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
        self._format_example(self._color('green', '✓'), example)

    def example_failed(self, example):
        self._format_example(self._color('red', '✗'), example)
        with indent((self._depth(example) + 1) * 2):
            puts(self._color('red', str(example.error.exception)))

    def _depth(self, example):
        depth = 0
        current = example.parent
        while current is not None:
            depth += 1
            current = current.parent

        return depth

    def example_pending(self, example):
        self._format_example(self._color('yellow', '✗'), example)

    def _format_example(self, symbol, example):
        puts('  ' * self._depth(example) + symbol + ' ' + example.name + self._format_slow_test(example))

    def _format_slow_test(self, example):
        seconds = example.elapsed_time.total_seconds()
        color_name = None

        if seconds > self.settings.slow_test_threshold:
            color_name = 'yellow'

            if seconds > 5 * self.settings.slow_test_threshold:
                color_name = 'red'

        if color_name is not None:
            return self._color(color_name, ' (' + self._format_duration(example.elapsed_time) + ')')

        return ''

    def example_group_started(self, example_group):
        self._format_example_group(example_group, 'white')

    def example_group_finished(self, example_group):
        if example_group.parent is None:
            puts()

    def example_group_pending(self, example_group):
        self._format_example_group(example_group, 'yellow')

    def _format_example_group(self, example_group, color_name):
        puts('  ' * self._depth(example_group) + self._color(color_name, example_group.name))

    def summary(self, duration, example_count, failed_count, pending_count):
        duration = self._format_duration(duration)
        if failed_count != 0:
            puts(self._color('red', "%d examples failed of %d ran in %s" % (failed_count, example_count, duration)))
        elif pending_count != 0:
            puts(self._color('yellow', "%d examples ran (%d pending) in %s" % (example_count, pending_count, duration)))
        else:
            puts(self._color('green', "%d examples ran in %s" % (example_count, duration)))

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
                    puts(self._color('red', 'Failure/Error: %s' % self._format_failing_expectation(failed)))
                    puts(self._color('red', self._format_traceback(failed)))
                    puts()

    def _format_full_example_name(self, example):
        result = [example.name]

        current = example
        while current.parent:
            result.append(current.parent.name)
            current = current.parent

        result.reverse()
        return ' '.join(result)

    def _format_failing_expectation(self, example_):
        tb = self._traceback(example_)
        filename = inspect.getsourcefile(tb)

        return """{filename} {source_line}
    {exc_type}: {exc_msg}
        """.format(
            filename=filename,
            source_line=open(filename).read().splitlines()[tb.tb_lineno-1].strip(),
            exc_type=type(example_.error.exception).__name__,
            exc_msg=str(example_.error.exception)
        )

    def _traceback(self, example_):
        return example_.error.traceback.tb_next

    def _format_traceback(self, example_):
        tb = self._traceback(example_)
        return ''.join([message[2:] for message in reversed(traceback.format_tb(tb))])

    def _color(self, name, text):
        if not self.settings.no_color and sys.stdout.isatty():
            return getattr(colored, name)(text)
        return text


class ProgressFormatter(DocumentationFormatter):

    def example_passed(self, example):
        puts(self._color('green', '.'), newline=False)

    def example_failed(self, example):
        puts(self._color('red', 'F'), newline=False)

    def example_pending(self, example):
        puts(self._color('yellow', '*'), newline=False)

    def example_group_started(self, example_group):
        pass

    def example_group_finished(self, example_group):
        pass

    def example_group_pending(self, example_group):
        pass

    def summary(self, duration, example_count, failed_count, pending_count):
        puts()
        puts()
        super(ProgressFormatter, self).summary(duration, example_count, failed_count, pending_count)
