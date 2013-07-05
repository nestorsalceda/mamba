class Runner(object):

    def __init__(self):
        self.has_failed_specs = False

    def run(self, specs):
        for spec in specs:
            spec.run()

            if spec.failed:
                self.has_failed_specs = True
