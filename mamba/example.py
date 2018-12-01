# -*- coding: utf-8 -*-

from datetime import datetime

from mamba import runnable


class Example(runnable.Runnable):

    # TODO: Remove parent parameter, it's only used for testing purposes
    def __init__(self, test, parent=None, tags=None, module=None):
        super(Example, self).__init__(parent=parent, tags=tags)
        self.module = module
        self.test = test
        self.was_run = False

    def execute(self, reporter, execution_context, tags=None):
        assert self.parent is not None
        if not self.included_in_execution(tags):
            return

        self._start(reporter)

        if self.error is None:
            self.parent.execute_hook('before_each', execution_context)

        if self.error is None:
            self._execute_test(execution_context)

        self.parent.execute_hook('after_each', execution_context)

        self._finish(reporter)

    def _start(self, reporter):
        self._begin = datetime.utcnow()
        reporter.example_started(self)

    def _execute_test(self, execution_context):
        try:
            if hasattr(self.test, 'im_func'):
                self.test.im_func(execution_context)
            else:
                self.test(execution_context)
        except Exception:
            self.fail()
        finally:
            self.was_run = True

    def _finish(self, reporter):
        self.elapsed_time = datetime.utcnow() - self._begin
        if self.failed():
            reporter.example_failed(self)
        else:
            reporter.example_passed(self)

    @property
    def name(self):
        return self.test._example_name

    @property
    def file(self):
        return self.module.__file__

    @property
    def classname(self):
        return self.module.__name__.replace('/', '.')


class PendingExample(Example):
    def execute(self, reporter, execution_context, tags=None):
        reporter.example_pending(self)
