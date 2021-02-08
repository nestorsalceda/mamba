import contextlib


__version__ = '0.11.2+gemfury'


__all__ = [
    "description", "_description", "fdescription",
    "describe", "_describe", "fdescribe",
    "it", "_it", "fit",
    "context", "_context", "fcontext",
]


class Noop(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return True


class BeforeAfter(object):
    def __init__(self):
        self.each = Noop()


def description(message, tag=None):
    """Create a new logical grouping of specs."""
    return Noop()


def _description(message, tag=None):
    """Create a new logical grouping of disabled specs."""
    return Noop()


def fdescription(message, tag=None):
    """Create a new logical grouping of focused specs."""
    return Noop()


def describe(message, tag=None):
    """Create a new logical grouping of specs."""
    return Noop()


def _describe(message, tag=None):
    """Create a new logical grouping of disabled specs."""
    return Noop()


def fdescribe(*args):
    """Create a new logical grouping of focused specs."""
    return Noop()


def it(message, tag=None):
    """Create a new spec."""
    raise NotImplementedError()


def _it(message, tag=None):
    """Create a new disabled spec."""
    raise NotImplementedError()


def fit(message, tag=None):
    """Create a new focused spec."""
    raise NotImplementedError()


def context(message, tag=None):
    """Create a new logical sub-grouping of specs."""
    return Noop()


def _context(message, tag=None):
    """Create a new logical sub-grouping of disabled specs."""
    return Noop()

def shared_context(message):
    """Create a new shared context."""
    return Noop()

def included_context(message):
    """Create a new included context."""
    return Noop()


def fcontext(message, tag=None):
    """Create a new logical sub-grouping of focused specs."""
    return Noop()


before = BeforeAfter()
after = BeforeAfter()
