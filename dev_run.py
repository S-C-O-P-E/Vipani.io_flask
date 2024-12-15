import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

class FlaskDevHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.process = None
        self.restart_process()

    def restart_process(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen([sys.executable, 'run.py'])

    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(('.py', '.env')):
            print(f"Detected change in {event.src_path}. Restarting...")
            self.restart_process()

def run_flask_dev_server():
    path = '.'
    event_handler = FlaskDevHandler(None)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    run_flask_dev_server()