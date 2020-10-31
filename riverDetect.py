import cv2
import numpy as np


class DetectRivers:
    def find_rivermask(self, img):
        img = cv2.imread(img)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_range = np.array([2, 66, 70])
        upper_range = np.array([25, 180, 120])

        mask = cv2.inRange(hsv, lower_range, upper_range)

        kernel = np.ones((3, 3), np.uint8)
        mask_eroded = cv2.erode(mask, kernel, 1)

        kernel = np.ones((9, 9), np.uint8)
        mask_dilated = cv2.dilate(mask_eroded, kernel, 1)

        #cv2.imshow("Image", img)
        #cv2.imshow("Mask", mask)
        #cv2.imshow("Mask Eroded", maskEroded)
        #cv2.imshow("Mask Dilated", mask_dilated)

        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        return mask_dilated


