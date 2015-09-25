#!/usr/bin/python2
import praw
import sys
import argparse

watcher_choices = ["front", "new", "rising", "controversial", "inbox"]
comments_watchers = ["inbox"]
argparser = argparse.ArgumentParser()
argparser.add_argument("-ng", "--nogpio", help="don't use gpio port to notify", action="store_true")
argparser.add_argument("-w", "--watched", type=str, choices=watcher_choices, default="rising", help="choose watched section")
args = argparser.parse_args()

if args.nogpio is True:
    import notification.termonly.notifier as nt
else:
    try:
        import notification.gpio.notifier as nt
    except ImportError:
        print >> sys.stderr, "Can't import gpio module, use term-only mode"
        import notification.termonly.notifier as nt
watch_choice = watcher_choices.index(args.watched)


user_agent = "linux:Rising Watch:v0.0.1 (by /u/not_da_bot)"
r = praw.Reddit(user_agent=user_agent, cache_timeout=1)
post_retrievers = [r.get_front_page, r.get_new, r.get_rising, r.get_controversial, r.get_inbox]
cooldown_times = [60, 2, 2, 10, 2]

post_retriever = post_retrievers[watch_choice]
cooldown_time = cooldown_times[watch_choice]
rising_retrieve_limit = 10
notifier = nt.notify_comment if args.watched in comments_watchers else nt.notify


try:
    nt.init()
    r.login()
    last_ids = []
    while 1:
        nt.retrieve_on()
        ids_list = []
        new_posts = []
        posts = post_retriever(limit=rising_retrieve_limit)
        for post in posts:
            if post.id not in last_ids:
                new_posts.append(post)
            ids_list.append(post.id)
        last_ids = list(ids_list)
        if len(new_posts) != 0:
            notifier(new_posts)
        nt.cooldown(cooldown_time=cooldown_time)
except KeyboardInterrupt:
    print >> sys.stderr, "\nKeyboard Interruption\n"
except praw.errors.InvalidUserPass:
    print >> sys.stderr, "\nInvalid credentials\n"
except Exception,e:
    print >> sys.stderr, "\nUnexpected Exception\n"
    print >> sys.stderr, str(e)
finally:
    nt.close()
    print >> sys.stderr, "Bye"
