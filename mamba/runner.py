from mamba import reporters

class Runner(object):

    def __init__(self, reporter):
        self.reporter = reporter
        self.has_failed_specs = False

    def run(self, specs):
        for spec in specs:
            spec.run(self.reporter)

            if spec.failed:
                self.has_failed_specs = True
