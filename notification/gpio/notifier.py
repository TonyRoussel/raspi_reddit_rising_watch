import RPi.GPIO as GPIO
import time


gpio_retrieve = 7
gpio_new_rise = 11
gpio_comm_num = 13
gpio_nsfw = 15

gpio_list = [gpio_new_rise, gpio_retrieve, gpio_comm_num, gpio_nsfw]

time_new_rise = 1.
time_between_notif = 1/4.

def init():
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


def close():
    for gpio in gpio_list:
        GPIO.output(gpio, GPIO.LOW)
    GPIO.cleanup()
    return


def notify(submissions):
    for submission in submissions:
        time.sleep(time_between_notif)
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


def retrieve_on():
    GPIO.output(gpio_retrieve, GPIO.HIGH)
    return


def cooldown(cooldown_time=2):
    GPIO.output(gpio_retrieve, GPIO.LOW)
    time.sleep(cooldown_time)
    return
