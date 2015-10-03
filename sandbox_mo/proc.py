__author__ = 'amaury'

import subprocess
import time
import sys

class Timeout(Exception):
    pass

def run(command, timeout=10):
    proc = subprocess.Popen("./timeout.sh "+timeout+" "+command, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    poll_seconds = .250
    deadline = time.time()+timeout
    while time.time() < deadline and proc.poll() == None:
        time.sleep(poll_seconds)

    if proc.poll() == None:
        if float(sys.version[:3]) >= 2.6:
            proc.terminate()
        raise Timeout()

    stdout, stderr = proc.communicate()
    return stdout, stderr, proc.returncode

if __name__=="__main__":
    print run(["ls", "-l"])
    print run(["find", "/"], timeout=3) #should timeout