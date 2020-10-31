import numpy as np
import cv2
import riverDetect
import pixelCounter

def find_river(self, img):
    return riverDetect.DetectRivers.find_rivermask(None, img)


riverBefore = find_river(None, "beforeflood.png")
riverAfter = find_river(None, "afterflood.png")

pixelDifference = pixelCounter.CompareAreas.find_diffrence(None, riverBefore, riverAfter)
print(pixelDifference)