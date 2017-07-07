import os
import signal
import time
import re

FIFO = input("Input FIFO: ")


def receive_new_cmd():

    ESC="\33"
    GS="\35"
    RS="\36"
    US="\37"

    def split_escaped(string, delim):
        split = re.split('(?<!{}){}'.format(ESC, delim), string)
        return [string.replace(ESC+delim, delim) for string in split]
    
    with open(FIFO) as f:
        raw = f.read()

    # cmd, env = raw.split(GS)
    # env = env.split(RS)[:-1]
    # env = dict([kv.split(US) for kv in env])

    cmd, env = split_escaped(raw, GS)
    env = split_escaped(env, RS)[:-1]
    env = dict([split_escaped(kv, US) for kv in env])

    print "cmd:", cmd
    print "env:", env


def handler(signum, stack):
    try:
        handle = {
            signal.SIGIO: receive_new_cmd,
        }[signum]
    except KeyError:
        raise RuntimeError("Unexpected signal: {}".format(signum))
    else:
        handle()
    

print 'My PID is:', os.getpid()

signal.signal(signal.SIGIO, handler)

while(True):
    print "sleeping."
    time.sleep(3)