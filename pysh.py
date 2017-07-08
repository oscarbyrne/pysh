import os
import signal
import time
import re

FIFO = input("Input FIFO: ")


def receive_new_cmd():

    with open(FIFO) as f:
        raw = f.read()

    ESC="\33"
    GS="\35"
    RS="\36"
    US="\37"

    def escaped_split(string, sep):
        unesc = '(?<!{}){}'.format(ESC, sep)
        return re.split(unesc, string)

    def unescape(string):
        return string \
            .replace(ESC+GS, GS) \
            .replace(ESC+RS, RS) \
            .replace(ESC+US, US)

    cmd, env = escaped_split(raw, GS)
    env = escaped_split(env, RS)[:-1]
    env = env[:-1]
    env = [escaped_split(kv, US) for kv in env]
    env = {unescape(k): unescape(v) for k, v in env}

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