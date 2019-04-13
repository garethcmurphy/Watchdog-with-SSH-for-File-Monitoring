#!/usr/bin/env python3
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import paramiko
from paramiko import SSHClient
from scp import SCPClient
import json

class MyEventHandler(FileSystemEventHandler):
    def __init__(self):
        pass

    def on_created(self, event):
        configfile="../config.json"
        if (configfile):
            with open(configfile, 'r') as f:
                config = json.load(f)
        ssh = SSHClient()
        k = paramiko.Ed25519Key.from_private_key_file(config["privatekey"])
        ssh.load_system_host_keys()
        ssh.connect(hostname=config["hostname"],username=config["username"],pkey=k)
        scp = SCPClient(ssh.get_transport())
        scp.put(event.src_path)

        print("e=", event)
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
