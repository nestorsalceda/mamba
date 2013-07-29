from functools import partial

from mamba.example_group import ExampleGroup
from mamba.example import Example

IRRELEVANT_SUBJECT='irrelevant subject'


def an_example_group(subject=IRRELEVANT_SUBJECT):
    return ExampleGroup(IRRELEVANT_SUBJECT)


def an_example(context):
    return Example(partial(_successful_test, context))


def _successful_test(context):
    context.was_run = True


def a_failing_example():
    return Example(_failing_test)


def _failing_test():
    raise ValueError()
