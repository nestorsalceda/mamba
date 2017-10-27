from functools import partial

from mamba.example_group import ExampleGroup, PendingExampleGroup
from mamba.example import Example, PendingExample

IRRELEVANT_DESCRIPTION='any description'


def an_example_group(description=IRRELEVANT_DESCRIPTION):
    return ExampleGroup(IRRELEVANT_DESCRIPTION)


def a_pending_example_group(description=IRRELEVANT_DESCRIPTION):
    return PendingExampleGroup(IRRELEVANT_DESCRIPTION)


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

