import contextlib


__version__ = '0.10'


def description(message):
    pass


def _description(message):
    pass


def fdescription(message):
    pass


def describe(message):
    pass


def _describe(message):
    pass


def fdescribe(message):
    pass


def it(message):
    pass


def _it(message):
    pass


def fit(message):
    pass


def context(message):
    pass


def _context(message):
    pass


def fcontext(message):
    pass


def shared_context(message):
    pass


def included_context(message):
    pass


@contextlib.contextmanager
def before():
    pass


@contextlib.contextmanager
def before_all():
    pass


@contextlib.contextmanager
def after():
    pass


@contextlib.contextmanager
def after_all():
    pass
