#!/usr/bin/python2
import praw
import sys
import time
import RPi.GPIO as GPIO


gpio_new_rise = 7
gpio_retrive = 11

gpio_list = [gpio_new_rise, gpio_retrieve]


rising_retrieve_limit = 10
cooldown_time = 2


def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    for gpio in gpio_list:
        GPIO.setup(gpio, GPIO.OUT)
    return


def gpio_blink(pin, bton=1.):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(bton)
    GPIO.output(pin, GPIO.LOW)
    return


def close_gpio():
    for gpio in gpio_list:
        GPIO.output(gpio, GPIO.LOW)
    GPIO.cleanup()
    return


def cooldown(pin):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(cooldown_time)
    return


def notify(pin, count):
    for i in xrange(count):
        gpio_blink(pin, bton=1/4.)
        time.sleep(1/3.)
    return


try:
    init_gpio()
    user_agent = "linux:Rising Watch:v0.0.1 (by /u/not_da_bot)"
    r = praw.Reddit(user_agent=user_agent)
    last_ids = []
    r.login()
    while 1:
        GPIO.output(gpio_retrieve, GPIO.HIGH)
        new_count = 0
        ids_list = []
        rising = r.get_rising(limit=rising_retrieve_limit)
        for submission in rising:
            if submission.id not in last_ids:
                new_count = new_count + 1
            ids_list.append(submission.id)
        last_ids = list(ids_list)
        if new_count != 0:
            notify(gpio_new_rise, new_count)
        cooldown(gpio_retrieve)
except KeyboardInterrupt:
    print >> sys.stderr, "\nKeyboard Interruption\n"
except praw.errors.InvalidUserPass:
    print >> sys.stderr, "\nInvalid credentials\n"
except:
    print >> sys.stderr, "\nUnexpected Exception\n"
finally:
    close_gpio()
    print >> sys.stderr, "Bye"
