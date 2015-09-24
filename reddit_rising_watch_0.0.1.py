#!/usr/bin/python2
import praw
import sys
import time
import RPi.GPIO as GPIO


gpio_retrieve = 7
gpio_new_rise = 11
gpio_comm_num = 13
gpio_nsfw = 15

gpio_list = [gpio_new_rise, gpio_retrieve, gpio_comm_num, gpio_nsfw]

time_new_rise = 1.


rising_retrieve_limit = 10
cooldown_time = 2


def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    for gpio in gpio_list:
        GPIO.setup(gpio, GPIO.OUT)
    return


def gpio_blink(pin, bton=1., btoff=None):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(bton)
    GPIO.output(pin, GPIO.LOW)
    if btoff is not None:
        time.sleep(btoff)
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


def notify(submissions):
    for submission in submissions:
        title = submission.title.encode('utf-8')
        subreddit_name = submission.subreddit.display_name.encode('utf-8')
        comments_count = submission.num_comments
        nsfw = submission.over_18
        if not nsfw:
            print "- %s [/r/%s] (%d comments)" % (title, subreddit_name, comments_count)
        else:
            print "- %s [/r/%s] (%d comments) {NSFW}" % (title, subreddit_name, comments_count)
        if comments_count != 0:
            time_comm_num = time_new_rise / float(comments_count)
            GPIO.output((gpio_new_rise, gpio_nsfw), (GPIO.HIGH, GPIO.HIGH if nsfw else GPIO.LOW))
            for i in xrange(comments_count):
                gpio_blink(gpio_comm_num, bton=time_comm_num/2., btoff=time_comm_num/2.)
            GPIO.output((gpio_new_rise, gpio_nsfw), (GPIO.LOW, GPIO.LOW))
        else:
            gpio_blink(gpio_new_rise, bton=time_new_rise)
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
        new_submissions = []
        rising = r.get_rising(limit=rising_retrieve_limit)
        for submission in rising:
            if submission.id not in last_ids:
                new_submissions.append(submission)
            ids_list.append(submission.id)
        last_ids = list(ids_list)
        if len(new_submissions) != 0:
            notify(new_submissions)
        cooldown(gpio_retrieve)
except KeyboardInterrupt:
    print >> sys.stderr, "\nKeyboard Interruption\n"
except praw.errors.InvalidUserPass:
    print >> sys.stderr, "\nInvalid credentials\n"
except Exception,e:
    print >> sys.stderr, str(e)
except:
    print >> sys.stderr, "\nUnexpected Exception\n"
finally:
    close_gpio()
    print >> sys.stderr, "Bye"
