import sys
from time import sleep

while True:
    print 'neighbor 10.0.2.1 announce route 192.168.10.0/24 next-hop self'
    sys.stdout.flush()
    sleep(10)
    print 'neighbor 10.0.2.1 withdraw route 192.168.10.0/24 next-hop self'
    sys.stdout.flush()
    sleep(10)

