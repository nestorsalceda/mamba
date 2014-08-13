from functools import partial

from mamba.example_group import ExampleGroup, PendingExampleGroup
from mamba.example import Example, PendingExample

IRRELEVANT_SUBJECT='irrelevant subject'


def an_example_group(subject=IRRELEVANT_SUBJECT):
    return ExampleGroup(IRRELEVANT_SUBJECT)


def a_pending_example_group(subject=IRRELEVANT_SUBJECT):
    return PendingExampleGroup(IRRELEVANT_SUBJECT)


def an_example():
    return Example(_WithSuccessfulTest._successful_test, parent=an_example_group())


class _WithSuccessfulTest(object):
    def _successful_test(self):
        pass


def a_pending_example():
    return PendingExample(_WithSuccessfulTest._successful_test)


def a_failing_example():
    return Example(_WithFailingTest._failing_test)


class _WithFailingTest(object):
    def _failing_test(self):
        raise ValueError()

