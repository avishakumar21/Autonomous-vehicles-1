import subprocess
import sys

array = [1]*20
for scriptInstance in array:
    sys.stdout=open('result%s.txt' % scriptInstance,'w')
    subprocess.check_call(['python','highway.py'], \
		stdout=sys.stdout, stderr=subprocess.STDOUT)