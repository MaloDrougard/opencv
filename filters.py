import cv2
from os import path

static_dir = "/home/makem/Créations/Microscope/static"


def filter(frame):

    hight = len(frame)
    width = len(frame[0])

    ori_image_path = path.join(static_dir,"bier1.jpg")
    overlay = cv2.imread(ori_image_path)
    overlay = cv2.resize(overlay, (width, hight), interpolation = cv2.INTER_AREA)
 
    filtered = cv2.addWeighted(frame,0.4,overlay,0.4,0)

    return filtered
