import argparse
import thread
import sys
import tty
import termios


def check_positive_float(value):
    fvalue = float(value)
    if fvalue < 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive float value" % value)
    return fvalue


def list_unique_merge(l1, l2):
    for x in l2:
        if x not in l1:
            l1.append(x)
    return


def key_detect():
    char = [None]
    thread.start_new_thread(_keydetect_init, (char,))
    return char


def _keydetect_init(char):
    char[0] = _keydetect_core()


def _keydetect_core():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
