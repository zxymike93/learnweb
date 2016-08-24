#!/usr/bin/env python3

def log(*args, **kwargs):
    """
    用 log 代替 print
    """
    print('log', *args, **kwargs)