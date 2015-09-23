#!/usr/bin/python2
import praw
import sys
import time
import RPi.GPIO as GPIO


gpio_new_rise = 7
gpio_retrieve = 11

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


def notify(pin, titles):
    for title in titles:
        print "-", title.encode('utf-8')
        gpio_blink(pin, bton=1/4.)
        time.sleep(1/4.)
    print ""
    return


try:
    init_gpio()
    user_agent = "linux:Rising Watch:v0.0.1 (by /u/not_da_bot)"
    r = praw.Reddit(user_agent=user_agent, cache_timeout=1)
    last_ids = []
    r.login()
    while 1:
        GPIO.output(gpio_retrieve, GPIO.HIGH)
        ids_list = []
        new_titles = []
        rising = r.get_rising(limit=rising_retrieve_limit)
        for submission in rising:
            if submission.id not in last_ids:
                new_titles.append(submission.title)
            ids_list.append(submission.id)
        last_ids = list(ids_list)
        if len(new_titles) != 0:
            notify(gpio_new_rise, new_titles)
        cooldown(gpio_retrieve)
except KeyboardInterrupt:
    print >> sys.stderr, "\nKeyboard Interruption\n"
except praw.errors.InvalidUserPass:
    print >> sys.stderr, "\nInvalid credentials\n"
except Exception,e:
    print str(e)
except:
    print >> sys.stderr, "\nUnexpected Exception\n"
finally:
    close_gpio()
    print >> sys.stderr, "Bye"
