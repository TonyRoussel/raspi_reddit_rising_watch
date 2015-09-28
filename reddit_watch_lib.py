import argparse


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
