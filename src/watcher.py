from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DotfileEventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory:
            self.callback(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.callback(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.callback(event.src_path)


def start_watching(path, callback):
    event_handler = DotfileEventHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    return observer
