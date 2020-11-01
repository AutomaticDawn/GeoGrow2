import cv2
import numpy as np


class CompareAreas:
    def find_diffrence(self, img1, img2):

        bright_count1 = np.sum(np.array(img1) > 0)
        bright_count2 = np.sum(np.array(img2) > 0)

        change_percentage = (bright_count2/bright_count1) * 100 - 100
        return change_percentage
