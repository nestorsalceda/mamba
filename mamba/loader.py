import inspect

from mamba import spec


class _Context(object):
    pass


class describe(object):

    def __init__(self, subject):
        self.subject = subject
        self.locals_before = None

    def __enter__(self):
        frame = inspect.currentframe().f_back
        self.locals_before = set(frame.f_locals.keys())

        if 'specs' not in frame.f_locals:
            frame.f_locals['specs'] = []
            frame.f_locals['current_spec'] = None

        if frame.f_locals['current_spec'] is None:
            frame.f_locals['current_spec'] = spec.Suite(self.subject, skipped=self._skipped)
            frame.f_locals['specs'].append(frame.f_locals['current_spec'])
        else:
            current = spec.Suite(self.subject, skipped=self._skipped)
            frame.f_locals['current_spec'].append(current)
            frame.f_locals['current_spec'] = current

        return _Context()

    @property
    def _skipped(self):
        return getattr(self, 'skipped', False)

    def __exit__(self, type, value, traceback):
        frame = inspect.currentframe().f_back

        possible_specs = set(frame.f_locals.keys()) - self.locals_before

        for function in possible_specs:
            code = frame.f_locals[function]

            if self._is_non_private_function(function, code) and not self._is_registered(code):
                self._register(code)
                if self._is_hook(code):
                    self._load_hooks(function, code, frame.f_locals['current_spec'])
                else:
                    frame.f_locals['current_spec'].append(spec.Spec(code, skipped=getattr(code, 'skipped', False)))

        frame.f_locals['current_spec'].specs.sort(key=lambda x: x.source_line)
        frame.f_locals['current_spec'] = frame.f_locals['current_spec'].parent

    def _is_non_private_function(self, function, code):
        return callable(code) and not function.startswith('_')

    def _is_registered(self, code):
        return getattr(code, '_registered', False)

    def _register(self, code):
        code._registered = True

    def _is_hook(self, function):
        return getattr(function, 'hook', [])

    def _load_hooks(self, function, code, current_spec):
        current_spec.hooks['%s_%s' % (code.hook['where'], code.hook['when'])] = code

context = describe
