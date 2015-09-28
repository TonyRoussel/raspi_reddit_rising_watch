import argparse


def check_positive_float(value):
    fvalue = float(value)
    if fvalue < 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive float value" % value)
    return fvalue
