import numpy as np
import cv2
import riverDetect
import pixelCounter


def switcher_func(arg):  # Switch funkcija za check_for_flood()
    switcher = {
        -1: "Possible drought",
        0: "Everything is chill",
        1: "Slight increase",
        2: "Keep an eye out",
        3: "Flood"
    }
    msg = switcher.get(arg, lambda: "Invalid month")
    return msg


def display_message_to_user(message):  # Ovde cemo ubaciti stvari koje ce da funkcionisu sa GUI-em
    print(message)


def check_for_flood():  # Provera izmedju beforeflood.png i afterflood.png za poplavom
    river_before = riverDetect.DetectRivers.find_rivermask(None, "beforeflood.png")
    river_after = riverDetect.DetectRivers.find_rivermask(None, "afterflood.png")

    pixel_difference = pixelCounter.CompareAreas.find_diffrence(None, river_before, river_after)
    pixel_difference = float("{:.2f}".format(pixel_difference))
    print("River level increase by", pixel_difference, "%")

    if pixel_difference > 100:
        alert_level_counter = 3
    elif pixel_difference > 50:
        alert_level_counter = 2
    elif pixel_difference > 0:
        alert_level_counter = 1
    elif pixel_difference < -50:
        alert_level_counter = -1
    else:
        alert_level_counter = 0

    return alert_level_counter


# Ovde krece program
alert_level = check_for_flood()
print(switcher_func(alert_level))
