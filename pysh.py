import os
import signal
import time
import re
import json
import pprint

FIFO = input("Input FIFO: ")


def receive_payload():
    with open(FIFO) as f:
        raw = f.read()
    env = json.loads(raw, strict=False) # allow control characters
    cmd = env['PYSH_COMMAND']
    return cmd, env

def handle_IO():
    cmd, env = receive_payload()
    # pysh_env = translate_env(env)


def handler(signum, stack):
    try:
        handle = {
            signal.SIGIO: handle_IO,
        }[signum]
    except KeyError:
        raise RuntimeError("Unexpected signal: {}".format(signum))
    else:
        handle()
    

print "My PID is:", os.getpid()

signal.signal(signal.SIGIO, handler)

while(True):
    print "sleeping."
    time.sleep(3)