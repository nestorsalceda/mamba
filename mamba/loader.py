import inspect

from mamba import spec


class _Context(object):
    pass


class describe(object):

    def __init__(self, subject):
        self.subject = subject
        self.locals_before = None

    def __enter__(self):
        frame = inspect.currentframe(1)
        self.locals_before = set(frame.f_locals.keys())

        if 'specs' not in frame.f_locals:
            frame.f_locals['specs'] = []
            frame.f_locals['current_spec'] = None

        if frame.f_locals['current_spec'] is None:
            frame.f_locals['current_spec'] = spec.Suite(self.subject)
            frame.f_locals['specs'].append(frame.f_locals['current_spec'])
        else:
            current = spec.Suite(self.subject)
            frame.f_locals['current_spec'].append(current)
            frame.f_locals['current_spec'] = current

        return _Context()

    def __exit__(self, type, value, traceback):
        frame = inspect.currentframe(1)

        possible_specs = set(frame.f_locals.keys()) - self.locals_before

        for key in possible_specs:
            value = frame.f_locals[key]

            if not callable(value) or key.startswith('_'):
                continue

            if getattr(value, '_registered', False):
                continue

            frame.f_locals['current_spec'].append(spec.Spec(value))
            value._registered = True


        frame.f_locals['current_spec'].specs.sort(key=lambda x: x.source_line())
        frame.f_locals['current_spec'] = frame.f_locals['current_spec'].parent


context = describe
