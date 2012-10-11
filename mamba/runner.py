class Runner(object):

    def run(self, module):
        for spec in module.specs:
            spec.run()
