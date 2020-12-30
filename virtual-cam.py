#!/usr/bin/python3

import os
import sys
import cv2
import fcntl
from v4l2 import (
    v4l2_format, VIDIOC_G_FMT, V4L2_BUF_TYPE_VIDEO_OUTPUT, V4L2_PIX_FMT_RGB24,
    V4L2_FIELD_NONE, VIDIOC_S_FMT
)

from utils import InputCamera, OutputVideo, GUIWindow
from filters import filter

SIZE = (640,480)
VIDEO_IN = "/dev/video0"
VIDEO_OUT = "/dev/video6"



def main():
    # open and configure input camera

    cam = InputCamera(VIDEO_IN, SIZE)
    out = OutputVideo(VIDEO_OUT, SIZE)

    gui = GUIWindow("Preview")

    while True:
        # grab frame
        if not cam.dev.grab():
            print("ERROR: could not read from camera!")
            break

        frame = cam.dev.retrieve()[1]

        filtered = filter(frame)

        # show frame
        gui.show(filtered)


        # write frame to output device
        #out.write(frame)
        
        # wait for user to finish program pressing ESC
        if cv2.waitKey(10) == 27:
            break

    print("\n\nFinish, bye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
