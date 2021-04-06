import cv2
import numpy as np


class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.colorMethod = None
        self.frame_to_display = None

    def __del__(self):
        self.video.release()

    def set_color_method(self, colorMethod):
        if colorMethod == "gray":
            self.colorMethod = cv2.COLOR_BGR2GRAY

    def get_frame(self):
        grabbed, frame = self.video.read()
        width = int(self.video.get(3))*2
        height = int(self.video.get(4))

        # _, clean_jpeg = cv2.imencode('.jpg', frame)
        # clean = clean_jpeg.tobytes()
        if self.colorMethod is not None:
            processed = cv2.cvtColor(frame, self.colorMethod)
            print(processed.shape)
        else:
            processed = frame

        output = np.zeros((height, width, frame.shape[2]), np.uint8)
        output[:height, :width // 2] = frame
        output[:height, width // 2:] = processed
        _, jpeg = cv2.imencode('.jpg', output)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')