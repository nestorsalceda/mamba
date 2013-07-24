import sys
import inspect
from datetime import datetime, timedelta


class _Runnable(object):

    def run(self, reporter):
        raise NotImplementedError()

    @property
    def elapsed_time(self):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def depth(self):
        if self.parent is None:
            return 0

        return self.parent.depth + 1

    @property
    def source_line(self):
        return float('inf')

    def run_hook(self, hook):
        raise NotImplementedError()

    @property
    def failed(self):
        raise NotImplementedError()

    @property
    def pending(self):
        raise NotImplementedError()

    @pending.setter
    def pending(self, value):
        raise NotImplementedError()

    @property
    def exception(self):
        raise NotImplementedError()

    @exception.setter
    def exception(self, value):
        raise NotImplementedError()

    @property
    def traceback(self):
        raise NotImplementedError()

    @traceback.setter
    def traceback(self, value):
        raise NotImplementedError()


class Spec(_Runnable):

    def __init__(self, test, parent=None, pending=False):
        self.test = test
        self.parent = parent
        self.pending = pending
        self._exception = None
        self._traceback = None
        self._elapsed_time = timedelta(0)

    def run(self, reporter):
        reporter.spec_started(self)
        try:
            begin = datetime.utcnow()
            if self.pending:
                reporter.spec_pending(self)
            else:
                self._run_inner_test(reporter)
        except Exception as exception:
            self._set_exception_from_inner_test()
            reporter.spec_failed(self)
        finally:
            self._elapsed_time = datetime.utcnow() - begin

    def _run_inner_test(self, reporter):
        self.run_hook('before_each')
        self.test()
        self.run_hook('after_each')
        reporter.spec_passed(self)

    def _set_exception_from_inner_test(self):
        type_, value, traceback = sys.exc_info()
        self.exception = value
        self.traceback = traceback

    def run_hook(self, hook):
        for parent in self._parents:
            parent.run_hook(hook)

    @property
    def _parents(self):
        parents = []
        parent = self.parent
        while parent:
            parents.append(parent)
            parent = parent.parent

        return reversed(parents)

    @property
    def elapsed_time(self):
        return self._elapsed_time

    @property
    def name(self):
        return self.test.__name__

    @property
    def source_line(self):
        return inspect.getsourcelines(self.test)[1]

    @property
    def failed(self):
        return self.exception is not None

    @property
    def pending(self):
        if self.parent:
            return self._pending or self.parent.pending
        return self._pending

    @pending.setter
    def pending(self, value):
        self._pending = value

    @property
    def exception(self):
        return self._exception

    @exception.setter
    def exception(self, value):
        self._exception = value

    @property
    def traceback(self):
        return self._traceback

    @traceback.setter
    def traceback(self, value):
        self._traceback = value


class SpecGroup(_Runnable):

    def __init__(self, subject, parent=None, pending=False, context=None):
        self.subject = subject
        self.specs = []
        self.parent = parent
        self.pending = pending
        self.context = context
        self.hooks = {'before_each': [], 'after_each': [], 'before_all': [], 'after_all': []}
        self._elapsed_time = timedelta(0)

    def run(self, reporter):
        self._register_subject_creation_in_before_each_hook()
        self._run_specs(reporter)

    def _register_subject_creation_in_before_each_hook(self):
        if self._can_create_subject():
            self.hooks['before_each'].insert(0, self._create_subject)

    def _can_create_subject(self):
        if not self.subject_is_class:
            return False

        try:
            self.subject()
            return True
        except:
            return False

    def _create_subject(self):
        try:
            self.context.subject = self.subject()
        except:
            pass

    def _run_specs(self, reporter):
        reporter.spec_group_started(self)
        try:
            begin = datetime.utcnow()
            self._run_inner_specs(reporter)
        except Exception as exception:
            self.exception = exception
        finally:
            self._elapsed_time = datetime.utcnow() - begin
            reporter.spec_group_finished(self)

    def _run_inner_specs(self, reporter):
        self.run_hook('before_all')
        for spec in self.specs:
            spec.run(reporter)
        self.run_hook('after_all')

    def run_hook(self, hook):
        for registered in self.hooks.get(hook, []):
            if callable(registered):
                registered()

    @property
    def elapsed_time(self):
        return self._elapsed_time

    @property
    def name(self):
        if self.subject_is_class:
            return self.subject.__name__
        return self.subject

    def append(self, spec):
        self.specs.append(spec)
        spec.parent = self

    @property
    def failed(self):
        return any(spec.failed for spec in self.specs)

    @property
    def pending(self):
        if self.parent:
            return self._pending or self.parent.pending
        return self._pending

    @pending.setter
    def pending(self, value):
        self._pending = value

    @property
    def exception(self):
        return self._exception

    @exception.setter
    def exception(self, value):
        self._exception = value

        for spec in self.specs:
            spec.exception = value

    @property
    def subject_is_class(self):
        return inspect.isclass(self.subject)
