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


class Spec(_Runnable):

    def __init__(self, test, parent=None, skipped=False):
        self.test = test
        self.parent = parent
        self.skipped = skipped
        self._exception_caught = None
        self._elapsed_time = timedelta(0)

    def run(self):

        try:
            begin = datetime.utcnow()
            self.run_hook('before_each')
            if not self.skipped:
                self.test()
            self.run_hook('after_each')
        except Exception as exception:
            self._exception_caught = exception
        finally:
            self._elapsed_time = datetime.utcnow() - begin

    def run_hook(self, hook):
        for parent in self._parents:
            if callable(parent.hooks.get(hook, None)):
                parent.hooks[hook]()

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

    def exception_caught(self):
        return self._exception_caught

    @property
    def name(self):
        return self.test.__name__

    @property
    def source_line(self):
        return inspect.getsourcelines(self.test)[1]

    @property
    def failed(self):
        return self.exception_caught() is not None

    @property
    def skipped(self):
        if self.parent:
            return self._skipped or self.parent.skipped
        return self._skipped

    @skipped.setter
    def skipped(self, value):
        self._skipped = value


class Suite(_Runnable):

    def __init__(self, subject, parent=None, skipped=False):
        self.subject = subject
        self.specs = []
        self.parent = parent
        self.skipped = skipped
        self.hooks = {'before_each': None, 'after_each': None, 'before_all': None, 'after_all': None}
        self._elapsed_time = timedelta(0)

    def run(self):
        begin = datetime.utcnow()
        self.run_hook('before_all')
        if not self.skipped:
            for spec in self.specs:
                spec.run()
        self.run_hook('after_all')
        self._elapsed_time = datetime.utcnow() - begin

    def run_hook(self, hook):
        if callable(self.hooks.get(hook, None)):
            self.hooks[hook]()

    @property
    def elapsed_time(self):
        return self._elapsed_time

    @property
    def name(self):
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
