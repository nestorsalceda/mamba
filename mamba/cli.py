# -*- coding: utf-8 -*-

import sys
import imp

from mamba import formatters
from mamba.runner import Runner


def main():
    formatter = formatters.DocumentationFormatter()
    runner = Runner(formatter)

    for file_ in sys.argv[1:]:
        module = imp.load_source(file_.replace('.py', ''), file_)
        runner.run(module)

    formatter.format_summary()

    if runner.has_failed_tests:
        sys.exit(1)


if __name__ == '__main__':
    main()
