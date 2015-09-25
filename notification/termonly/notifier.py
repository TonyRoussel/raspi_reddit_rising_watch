import time
import string

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


def reindent(s, numSpaces):
    s = string.split(s, '\n')
    s = [(numSpaces * ' ') + string.lstrip(line) for line in s]
    s = string.join(s, '\n')
    return s


def notify_comment(posts):
    for post in posts:
        subject = post.subject.encode('utf-8')
        author = post.author.name.encode('utf-8')
        body = post.body.encode('utf-8')
        if post.was_comment:
            subreddit = post.subreddit.display_name.encode('utf-8')
            title = post.link_title.encode('utf-8')
            print "- %s | %s [/r/%s]\n\t%s\n%s" % (subject, title, subreddit, reindent(body, 8), reindent(author, 4))
        else:
            print "- %s\n%s\n%s" % (subject, reindent(body, 8), reindent(author, 4))
        print ""
    print ""
    return


def retrieve_on():
    return


def cooldown(cooldown_time=2):
    time.sleep(cooldown_time)
    return
