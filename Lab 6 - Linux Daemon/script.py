import time
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from daemon import DaemonContext

def setup_logging():
    logging.basicConfig(
        filename='/var/log/file_monitor.log',
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
    )

class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path)
        logging.info(f'File created: {filename}')

def monitor_directory(directory):
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    directory_to_monitor = "/path/to/monitored_directory"

    with DaemonContext(
        working_directory=directory_to_monitor,
        stdout=open('/var/log/daemon_stdout.log', 'w+'),
        stderr=open('/var/log/daemon_stderr.log', 'w+')
    ):
        setup_logging()
        monitor_directory(directory_to_monitor)
