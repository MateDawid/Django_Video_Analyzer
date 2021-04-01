import cv2
import threading
import numpy as np


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.frame = None
        self.processed_image = self.frame
        self.cvtColorMethod = None

    def __del__(self):
        self.video.release()

    def get_clean_frame(self):
        grabbed, self.frame = self.video.read()
        _, jpeg = cv2.imencode('.jpg', self.frame)
        return jpeg.tobytes()

    def get_gray_frame(self):
        self.cvtColorMethod = cv2.COLOR_BGR2GRAY
        grabbed, self.frame = self.video.read()

        _, jpeg = cv2.imencode('.jpg', cv2.cvtColor(self.frame, self.cvtColorMethod))
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_gray_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')