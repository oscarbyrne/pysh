import sys
import os
import signal
import json
import time
import logging
import pprint


def receive_payload():
    with open(FIFO, 'r') as f:
        raw = f.read()
    env = json.loads(raw, strict=False) # allow control characters
    cmd = env['PYSH_COMMAND']
    return cmd, env

def handle_IO():
    cmd, env = receive_payload()
    logging.debug(pprint.pformat(cmd))
    logging.debug(pprint.pformat(env))
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

def main():
    while(True):
        pass


if __name__ == '__main__':

    PYSH_SESSION = sys.argv[1]
    PDIR = "/tmp/pysh/{}".format(PYSH_SESSION)
    FIFO = "{}/PYSH_PIPE".format(PDIR)
    PLOG = "{}/PYSH_LOG".format(PDIR)

    logging.basicConfig(filename=PLOG,level=logging.DEBUG)
    signal.signal(signal.SIGIO, handler)

    main()

