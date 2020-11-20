#!/usr/bin/python3

import base64
import itertools

def dec(data, key):
    return base64.b64decode(''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(data, itertools.cycle(key))))
