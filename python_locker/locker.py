#!/usr/bin/env python3

import os
import fcntl
import time

def portable_lock(fp):
    fcntl.flock(fp.fileno(), fcntl.LOCK_EX)

def portable_unlock(fp):
    fcntl.flock(fp.fileno(), fcntl.LOCK_UN)

class Locker:
    def __init__(self, lock_file_path="/dev/shm/lockfile.shm"):
        self.lock_file_path = lock_file_path
        if not os.path.exists(self.lock_file_path):
            with open(self.lock_file_path, "w") as f:
                f.write("")

    def __enter__(self):
        self.fp = open(self.lock_file_path)
        portable_lock(self.fp)

    def __exit__(self, _type, value, tb):
        portable_unlock(self.fp)
        self.fp.close()

if __name__ == "__main__":
    while True:
        print("trying to enter into exclusive mode")
        with Locker() as lock:
            print("exclusive mode entered!")
            for i in range(10):
                print(".", flush=True, end="")
                time.sleep(1)
            print()
            print("exiting exclusive mode")
        print("exclusive mode exited")
