import cv2
import numpy as np


class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.colorMethod = None
        self.processed = None

    def __del__(self):
        self.video.release()

    def detect_circles(self, image, dp=1, minDist=20, param1=50, param2=70, minRadius=20, maxRadius=100):
        # Convert to grayscale.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Blur using 3 * 3 kernel.
        gray_blurred = cv2.blur(gray, (3, 3))
        # Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(image=gray_blurred,
                                            method=cv2.HOUGH_GRADIENT,
                                            dp=dp,  # inverse resolution ratio
                                            minDist=minDist,  # min distance between two circles centers
                                            param1=param1,
                                            param2=param2,
                                            minRadius=minRadius,
                                            maxRadius=maxRadius)
        if detected_circles is not None:

            # Convert the circle parameters a, b and r to round integers.
            detected_circles = np.uint16(np.around(detected_circles))

            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]

                # Draw the circumference of the circle.
                cv2.circle(image, (a, b), r, (0, 255, 0), 2)
                cv2.circle(image, (a, b), 1, (0, 0, 255), 3)

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
        _, frame = self.video.read()
        width = int(self.video.get(3))*2
        height = int(self.video.get(4))

        if self.colorMethod is not None:
            processed = cv2.cvtColor(frame, self.colorMethod)

        else:
            processed = frame.copy()
            # self.detect_circles(processed)

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