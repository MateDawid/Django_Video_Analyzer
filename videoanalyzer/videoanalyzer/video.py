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

    @staticmethod
    def get_text_size(text):
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 1, 2)
        return text_size

    @staticmethod
    def display_text(image, text, position, text_width, text_height):
        font = cv2.FONT_HERSHEY_DUPLEX
        x, y = position
        cv2.rectangle(image, (x, y), (x + text_width, y + text_height + 5), (255, 255, 255), -1)
        cv2.putText(image, text, (x, y + text_height), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

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
            #usunąć trzeci parametr z frame.shape?
            processed = frame

        output = np.zeros((height, width, frame.shape[2]), np.uint8)
        output[:height, :width // 2] = frame
        output[:height, width // 2:] = processed

        # getting texts sizes

        input_text_w, input_text_h = VideoCamera.get_text_size('INPUT')
        output_text_w, output_text_h = VideoCamera.get_text_size('OUTPUT')

        #displying texts backgrounds

        VideoCamera.display_text(output, 'INPUT', (0,0), input_text_w, input_text_h)
        VideoCamera.display_text(output, 'OUTPUT', (width//2, 0), output_text_w, output_text_h)

        #extract image to .jpg format
        _, jpeg = cv2.imencode('.jpg', output)

        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')