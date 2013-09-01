# -*- coding: utf-8 -*-

from mamba.infrastructure import is_python3

if not is_python3():
    import time
    from watchdog.observers import Observer
    from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler


    class FileWatcher(object):

        def __init__(self, runner):
            self.runner = runner

        def wait_for_events(self):
            event_handler = _RunnerEventHandler(self.runner)
            observer = Observer()
            observer.schedule(event_handler, path='.', recursive=True)
            observer.start()
            try:
                while True:
                    time.sleep(5)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()


    class _RunnerEventHandler(PatternMatchingEventHandler):

        def __init__(self, runner):
            super(_RunnerEventHandler, self).__init__(patterns=['*.py'])
            self.runner = runner

        def on_modified(self, event):
            self.runner.run()

        def on_deleted(self, event):
            self.runner.run()
