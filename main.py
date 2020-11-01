import numpy as np
import cv2
import riverDetect
import pixelCounter
import graphical_user_interface
import time

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
    river_before = riverDetect.DetectRivers.find_rivermask(None, "pictures/satellite/beforeflood.png")
    river_after = riverDetect.DetectRivers.find_rivermask(None, "pictures/satellite/afterflood.png")

    pixel_difference = pixelCounter.CompareAreas.find_diffrence(None, river_before, river_after)
    pixel_difference = float("{:.2f}".format(pixel_difference))


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

    comparison_level = get_saved_alert_level()
    if alert_level_counter > -3 & alert_level_counter < 3:
        alert_level_counter += comparison_level
    # save_alert_level(alert_level_counter)
    # Ovo odkomentarisati kada budemo imali api

    #print("River level increase by ", pixel_difference, "%")
    #print(switcher_func(alert_level_counter))

    msg1 = "River level increase by " + str(pixel_difference) + "%"
    msg2 = str(switcher_func(alert_level_counter))

    graphical_user_interface.PageOne.update(msg1 + "\n" + msg2)

    #return alert_level_counter


class CoordinatesManager:
    def save_new_coordinates(self, x_upper_left, y_upper_left, x_lower_right,
                             y_lower_right):  # Upisuje nove koordinate u text fajl
        f = open("saves/local_coordinates.txt", "w")
        if x_upper_left != "" or y_upper_left != "" or x_lower_right != "" or y_lower_right != "":
            coordinates = str(x_upper_left) + " " + str(y_upper_left) + " " + str(x_lower_right) + " " + str(y_lower_right)
            f.write(coordinates)
        else:
            graphical_user_interface.Coordinates.updateErrorText(None, "Error: Not all fields filled")
            #print("Error: Not all fields filled")
        f.close()

    def get_current_coordinates(self):  # Cita upisane koordinate iz text fajla
        f = open("saves/local_coordinates.txt", "r")
        user_coordinates = str(f.read())
        f.close()
        return user_coordinates


def save_alert_level(alert_level_for_write):  # Upisuje trenutni alert level u text fajl
    f = open("saves/previous_comparison.txt", "w")
    f.write(str(alert_level_for_write))
    f.close()


def get_saved_alert_level():  # Cita prethodni alert level iz text fajla
    f = open("saves/previous_comparison.txt", "w")
    try:
        previous_alert_level = f.read()
    except:
        previous_alert_level = 0
    f.close()
    return previous_alert_level


def get_current_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)


# START

save_alert_level(0)  # Ovo naravno skloniti kada api proradi

# alert_level = check_for_flood()
# CoordinatesManager.save_new_coordinates(None, 19.353790283203125, 44.19469759091441, 19.378938674926758, 44.17654094649196)
# print(get_current_coordinates())
