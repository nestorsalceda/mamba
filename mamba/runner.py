class Runner(object):

    def __init__(self, formatter):
        self.formatter = formatter
        self.has_failed_tests = False

    def run(self, module):
        for spec in module.specs:
            spec.run()
            self.formatter.format(spec)
            if spec.failed:
                self.has_failed_tests = True
