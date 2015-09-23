#!/usr/bin/python2
import praw
import sys
import time


def cooldown():
    print "cooldown on"
    time.sleep(2)
    print "cooldown off"
    return


def notify(count):
    print count
    return


rising_retrieve_limit=10

try:
    user_agent="linux:Rising Watch:v0.0.1 (by /u/not_da_bot)"
    r = praw.Reddit(user_agent=user_agent)
    last_ids = []
    r.login()
    while 1:
        new_count = 0
        ids_list = []
        rising = r.get_rising(limit=rising_retrieve_limit)
        for submission in rising:
            if submission.id not in last_ids:
                new_count = new_count + 1
            ids_list.append(submission.id)
        last_ids = list(ids_list)
        if new_count != 0:
            notify(new_count)
        cooldown()
except KeyboardInterrupt:
    print >> sys.stderr, "\nKeyboard Interruption\n"
except praw.errors.InvalidUserPass:
    print >> sys.stderr, "\nInvalid credentials\n"
except:
    print >> sys.stderr, "\nUnexpected Exception\n"
finally:
    print >> sys.stderr, "Bye"
