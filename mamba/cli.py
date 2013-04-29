# -*- coding: utf-8 -*-

import sys
import os
import imp

from mamba import formatters
from mamba.runner import Runner


def main():
    formatter = formatters.DocumentationFormatter()
    runner = Runner(formatter)

    for file_ in _specs():
        module = imp.load_source(file_.replace('.py', ''), file_)
        runner.run(module)

    formatter.format_summary()

    if runner.has_failed_specs:
        sys.exit(1)


def _specs():
    if len(sys.argv) == 1:
        collected = []
        for root, dirs, files in os.walk('spec'):
            collected.extend([os.path.join(root, file_) for file_ in files if file_.endswith('_spec.py')])
        collected.sort()
        return collected
    else:
        return sys.argv[1:]


if __name__ == '__main__':
    main()
