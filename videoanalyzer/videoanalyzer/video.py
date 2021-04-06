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
        grabbed, frame = self.video.read() #stay
        width = int(self.video.get(3))
        height = int(self.video.get(4))

        image = np.zeros(frame.shape, np.uint8)
        smaller_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        image[:height//2, :width//2] = smaller_frame
        _, jpeg = cv2.imencode('.jpg', image) #stay with frame
        return jpeg.tobytes()



        # clean = jpeg.tobytes()
        # if self.colorMethod is not None:
        #     _, processed_jpeg = cv2.imencode('.jpg', cv2.cvtColor(frame, self.colorMethod))
        #     processed = processed_jpeg.tobytes()
        # else:
        #     _, processed_jpeg = cv2.imencode('.jpg', frame)
        #     processed = processed_jpeg.tobytes()
        # return [clean, processed]



def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')