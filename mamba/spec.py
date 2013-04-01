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
        return 'inf'

class Spec(_Runnable):

    def __init__(self, test, parent=None):
        self.test = test
        self.parent = parent
        self._exception_caught = None
        self._elapsed_time = timedelta(0)

    def run(self):
        try:
            begin = datetime.utcnow()
            self.test()
        except Exception as exception:
            self._exception_caught = exception
        finally:
            self._elapsed_time = datetime.utcnow() - begin

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


class Suite(_Runnable):

    def __init__(self, subject, parent=None):
        self.subject = subject
        self.specs = []
        self.parent = parent

    def run(self):
        for spec in self.specs:
            spec.run()

    @property
    def elapsed_time(self):
        return sum([spec.elapsed_time for spec in self.specs], timedelta(0))

    @property
    def name(self):
        return self.subject

    def append(self, spec):
        self.specs.append(spec)
        spec.parent = self
