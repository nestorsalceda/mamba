import inspect

from mamba import spec


class _Context(object):
    pass


class describe(object):

    def __init__(self, subject):
        self.subject = subject
        self.locals_before = None
        self.hooks = ['before', 'after', 'before_all', 'after_all']

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

        for function in possible_specs:
            code = frame.f_locals[function]

            if self._is_non_private_function(function, code) and not self._was_already_registered(code):
                if self._is_hook(function):
                    self._load_hooks(function, code, frame.f_locals['current_spec'])
                else:
                    frame.f_locals['current_spec'].append(spec.Spec(code))
                    code._registered = True

        frame.f_locals['current_spec'].specs.sort(key=lambda x: x.source_line)
        frame.f_locals['current_spec'] = frame.f_locals['current_spec'].parent

    def _is_non_private_function(self, function, code):
        return callable(code) and not function.startswith('_')

    def _is_hook(self, function):
        return function.startswith(tuple(self.hooks))

    def _load_hooks(self, function, code, current_spec):
        if function in self.hooks:
            current_spec.hooks[function] = code
        else:
            splitted = function.split('_')
            if len(splitted) > 1 and splitted[1] == 'all':
                current_spec.hooks[splitted[0] + '_' + splitted[1]] = code
            else:
                current_spec.hooks[splitted[0]] = code

    def _was_already_registered(self, code):
        return getattr(code, '_registered', False)


context = describe
