class Runner(object):

    def __init__(self, formatter):
        self.formatter = formatter

    def run(self, module):
        for spec in module.specs:
            spec.run()
            self.formatter.format(spec)
