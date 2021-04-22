import cv2
import numpy as np


class VideoCamera:
    def __init__(
            self,
            # Circle detection
            shapeDetection=None,
            dp=None, minDist=None,
            param1=None, param2=None,
            minRadius=None,
            maxRadius=None,
            # Triangle detection
            kernelShape=None,
            approximation=None,
            maxArea=None
    ):
        self.video = cv2.VideoCapture(0)
        self.colorMethod = None
        self.processed = None
        self.colorDetection = None
        self.shapeDetection = shapeDetection
        # Circle detection variables
        self.dp = dp
        self.minDist = minDist
        self.param1 = param1
        self.param2 = param2
        self.minRadius = minRadius
        self.maxRadius = maxRadius
        self.kernelShape = kernelShape
        self.approximation = approximation
        self.maxArea = maxArea

    def __del__(self):
        self.video.release()

    def detect_circles(self, image):
        # Convert to grayscale.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Blur using 3 * 3 kernel.
        gray_blurred = cv2.blur(gray, (3, 3))
        # Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(image=gray_blurred,
                                            method=cv2.HOUGH_GRADIENT,
                                            dp=self.dp,  # inverse resolution ratio
                                            minDist=self.minDist,  # min distance between two circles centers
                                            param1=self.param1,
                                            param2=self.param2,
                                            minRadius=self.minRadius,
                                            maxRadius=self.maxRadius)
        if detected_circles is not None:

            # Convert the circle parameters a, b and r to round integers.
            detected_circles = np.uint16(np.around(detected_circles))

            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]

                # Draw the circumference of the circle.
                cv2.circle(image, (a, b), r, (0, 255, 0), 2)
                cv2.circle(image, (a, b), 1, (0, 0, 255), 3)

    def find_contours(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((self.kernelShape, self.kernelShape), np.uint8)
        erosion = cv2.erode(gray, kernel, iterations=1)
        dilation = cv2.dilate(erosion, kernel, iterations=1)
        blur = cv2.GaussianBlur(dilation, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def detect_triangles(self, image):
        for cnt in self.find_contours(image):
            area = cv2.contourArea(cnt)
            if area > self.maxArea:
                epsilon = self.approximation * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                if len(approx) == 3:
                    cv2.drawContours(image, [approx], 0, (0, 255, 0), -1)

    def detect_squares(self, image):
        for cnt in self.find_contours(image):
            area = cv2.contourArea(cnt)
            if area > self.maxArea:
                epsilon = self.approximation * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(approx)
                    circle_check = float(w) / h
                    if 0.95 <= circle_check < 1.05:
                        cv2.drawContours(image, [approx], 0, (0, 255, 0), -1)

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
        width = int(self.video.get(3)) * 2
        height = int(self.video.get(4))

        if self.shapeDetection == "circle":
            processed = frame.copy()
            self.detect_circles(processed)

        elif self.shapeDetection == "triangle":
            processed = frame.copy()
            self.detect_triangles(processed)

        elif self.shapeDetection == "square":
            processed = frame.copy()
            self.detect_squares(processed)

        else:
            processed = frame.copy()

        output = np.zeros((height, width, frame.shape[2]), np.uint8)
        output[:height, :width // 2] = frame
        output[:height, width // 2:] = processed

        # getting texts sizes

        input_text_w, input_text_h = VideoCamera.get_text_size('INPUT')
        output_text_w, output_text_h = VideoCamera.get_text_size('OUTPUT')

        # displying texts backgrounds

        VideoCamera.display_text(output, 'INPUT', (0, 0), input_text_w, input_text_h)
        VideoCamera.display_text(output, 'OUTPUT', (width // 2, 0), output_text_w, output_text_h)

        # extract image to .jpg format
        _, jpeg = cv2.imencode('.jpg', output)

        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
