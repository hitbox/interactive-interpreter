import logging
import os
import signal
import subprocess
import sys
import threading
import time

KEY = "RELOADER_RUNNING"
VALUE = "true"

def iter_module_files():
    for module in list(sys.modules.values()):
        if module is None:
            continue
        filename = getattr(module, "__file__", None)
        if filename:
            old = None
            while not os.path.isfile(filename):
                old = filename
                filename = os.path.dirname(filename)
                if filename == old:
                    break
            else:
                if filename[-4:] in (".pyc", ".pyo"):
                    filename = filename[:-1]
                yield filename

def getlogger():
    return logging.getLogger("reloader")

class Reloader:

    def restart_with_reloader(self):
        while True:
            getlogger().info("restarting")
            args = [sys.executable] + sys.argv
            env = os.environ.copy()
            env[KEY] = VALUE
            exitcode = subprocess.call(args, env=env)
            if exitcode != 3:
                return exitcode

    def run(self):
        mtimes = {}
        while True:
            for filename in iter_module_files():
                try:
                    mtime = os.stat(filename).st_mtime
                except OSError:
                    continue
                oldtime = mtimes.get(filename)
                if oldtime is None:
                    mtimes[filename] = mtime
                    continue
                elif mtime > oldtime:
                    self.trigger_reload(filename)
            time.sleep(1)

    def trigger_reload(self, filename):
        getlogger().info("detected change in %r" % filename)
        sys.exit(3)


def sigterm(signum, frame):
    sys.exit(0)

def run_with_reloader(func):
    reloader = Reloader()
    signal.signal(signal.SIGTERM, sigterm)
    try:
        if os.environ.get(KEY) == VALUE:
            thread = threading.Thread(target=func, daemon=True)
            thread.start()
            reloader.run()
        else:
            sys.exit(reloader.restart_with_reloader())
    except KeyboardInterrupt:
        pass

def stupidloop():
    while True:
        proof = "def"
        print("%.2f: My stupid loop is running! %r" % (time.time(), proof))
        time.sleep(1)

def main():
    logging.basicConfig(level=logging.INFO)
    run_with_reloader(stupidloop)

if __name__ == "__main__":
    main()
