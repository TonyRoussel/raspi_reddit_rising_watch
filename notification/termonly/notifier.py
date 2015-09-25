import time


def init():
    return


def close():
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
    print ""
    return


def retrieve_on():
    return


def cooldown(cooldown_time=2):
    time.sleep(cooldown_time)
    return
