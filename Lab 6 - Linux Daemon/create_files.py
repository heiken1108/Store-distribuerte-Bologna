import os
from datetime import datetime
import time
from daemon import DaemonContext

directory = "/path/to/monitored_directory"

def create_file():
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as _:
        pass
    print(f"Created file: {file_path}")

def run_daemon():
    while True:
        create_file()
        time.sleep(3600)

def start_daemon():
    with DaemonContext():
        run_daemon()

if __name__ == "__main__":
    start_daemon()