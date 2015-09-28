import RPi.GPIO as GPIO


gpio_clean_notif = 37

gpio_list = [gpio_clean_notif]

bouncetime_clean_notif = 100


def init():
    """/!\\ Assume that notification init already called /!\\"""
    for gpio in gpio_list:
        # Pulled up to avoid false detection.
        # Wired to connect to GND on button press.
        # So we'll be setting up falling edge detection for both
        GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    return


def reset_container(container):
    del container[:]


def init_notif_clean_callback(new_post_container):
    callback = lambda channel, container = new_post_container: reset_container(new_post_container)
    GPIO.add_event_callback(gpio_clean_notif, GPIO.FALLING, callback=callback, bouncetime=bouncetime_clean_notif)
