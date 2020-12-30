
import os
import fcntl
import uuid
import cv2
from v4l2 import (
    v4l2_format, VIDIOC_G_FMT, V4L2_BUF_TYPE_VIDEO_OUTPUT, V4L2_PIX_FMT_RGB24,
    V4L2_FIELD_NONE, VIDIOC_S_FMT
)


class InputCamera:
    def __init__(self, path, size):
        self.dev = cv2.VideoCapture(path)
        if not self.dev.isOpened():
            raise RuntimeError("could not open camera")

        self.dev.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.dev.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])

    def get(self):
        if not self.dev.grab():
            raise RuntimeError("could not read from camera")
        return self.dev.retrieve()[1]


class OutputVideo:
    def __init__(self, path, size):
        self.dev = os.open(path, os.O_RDWR)

        vid_format = v4l2_format()
        vid_format.type = V4L2_BUF_TYPE_VIDEO_OUTPUT
        if fcntl.ioctl(self.dev, VIDIOC_G_FMT, vid_format) < 0:
            raise RuntimeError("unable to get output video format")

        framesize = size[0] * size[1] * 3
        vid_format.fmt.pix.width = size[0]
        vid_format.fmt.pix.height = size[1]
        vid_format.fmt.pix.pixelformat = V4L2_PIX_FMT_RGB24
        vid_format.fmt.pix.sizeimage = framesize
        vid_format.fmt.pix.field = V4L2_FIELD_NONE

        if fcntl.ioctl(self.dev, VIDIOC_S_FMT, vid_format) < 0:
            raise RuntimeError("unable to set output video format")

    def write(self, frame):
        if os.write(self.dev, frame.data) < 0:
            raise RuntimeError("could not write to output device")


class GUIWindow:
    def __init__(self, title):
        self.input_handler = None
        self.name = uuid.uuid1().hex
        cv2.namedWindow(self.name)
        cv2.setWindowTitle(self.name, title)

    def set_input_handler(self, handler):
        self.input_handler = handler

    def show(self, frame):
        cv2.imshow(self.name, frame)

    def check_kb(self, timeout=10):
        code = cv2.waitKey(timeout)
        if code != -1:
            self.input_handler(code)
