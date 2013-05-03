import inspect
from datetime import datetime, timedelta


class _Runnable(object):

    def run(self):
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
    def skipped(self):
        raise NotImplementedError()

    @skipped.setter
    def skipped(self, value):
        raise NotImplementedError()

    @property
    def exception(self):
        raise NotImplementedError()

    @exception.setter
    def exception(self, value):
        raise NotImplementedError()


class Spec(_Runnable):

    def __init__(self, test, parent=None, skipped=False):
        self.test = test
        self.parent = parent
        self.skipped = skipped
        self._exception = None
        self._elapsed_time = timedelta(0)

    def run(self):
        try:
            begin = datetime.utcnow()
            self.run_hook('before_each')
            if not self.skipped:
                self.test()
            self.run_hook('after_each')
        except Exception as exception:
            self.exception = exception
        finally:
            self._elapsed_time = datetime.utcnow() - begin

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
    def skipped(self):
        if self.parent:
            return self._skipped or self.parent.skipped
        return self._skipped

    @skipped.setter
    def skipped(self, value):
        self._skipped = value

    @property
    def exception(self):
        return self._exception

    @exception.setter
    def exception(self, value):
        self._exception = value

class Suite(_Runnable):

    def __init__(self, subject, parent=None, skipped=False, context=None):
        self.subject = subject
        self.specs = []
        self.parent = parent
        self.skipped = skipped
        self.context = context
        self.hooks = {'before_each': [], 'after_each': [], 'before_all': [], 'after_all': []}
        self._elapsed_time = timedelta(0)

    def run(self):
        self._register_subject_creation_in_before_each_hook()
        self._run_specs()

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

    def _run_specs(self):
        try:
            begin = datetime.utcnow()
            self.run_hook('before_all')
            if not self.skipped:
                for spec in self.specs:
                    spec.run()
            self.run_hook('after_all')
        except Exception as exception:
            self.exception = exception
        finally:
            self._elapsed_time = datetime.utcnow() - begin

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
    def skipped(self):
        if self.parent:
            return self._skipped or self.parent.skipped
        return self._skipped

    @skipped.setter
    def skipped(self, value):
        self._skipped = value

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
