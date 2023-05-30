import sys
import subprocess

procs = []
for i in range(5):
    proc = subprocess.Popen([sys.executable, 'ddos2.py'])
    procs.append(proc)

for proc in procs:
    proc.wait()