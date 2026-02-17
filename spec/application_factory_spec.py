# -*- coding: utf-8 -*-

import os
import tempfile
from types import SimpleNamespace

from expects import expect, equal
from mamba import description, context, it

from mamba.application_factory import ApplicationFactory


def _arguments():
    return SimpleNamespace(
        slow=0.075,
        enable_coverage=False,
        coverage_file='.coverage',
        format='documentation',
        specs=['./spec', './specs'],
        no_color=False,
        tags=None
    )


with description(ApplicationFactory):
    with context('when loading spec helper'):
        with it('loads spec/spec_helper.py without requiring spec package'):
            with tempfile.TemporaryDirectory() as workdir:
                previous = os.getcwd()
                try:
                    os.chdir(workdir)
                    os.makedirs('spec')
                    with open('spec/spec_helper.py', 'w') as spec_helper:
                        spec_helper.write("def configure(settings):\n")
                        spec_helper.write("    settings.format = 'progress'\n")

                    app = ApplicationFactory(_arguments())
                    expect(app.settings.format).to(equal('progress'))
                finally:
                    os.chdir(previous)
