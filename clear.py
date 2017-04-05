import psutil
import os, signal

effects = ['direction_of_arrival_demo',
           'mic_energy',
           'micarray_recorder',
           'arc_demo',
           'everloop_demo']

for eff in effects:
	for proc in psutil.process_iter():
	    if proc.name() == eff:
	        print(proc)
			proc.kill()
			os.kill(proc.pid, signal.SIGKILL)
			break
