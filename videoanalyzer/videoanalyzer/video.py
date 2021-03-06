import cv2
import numpy as np
import os


class VideoCamera:
    def __init__(
            self,
            shape_detection=None,
            color_detection=None,
            face_detection=None,
            # Circle detection
            dp=None,
            min_dist=None,
            param1=None,
            param2=None,
            min_radius=None,
            max_radius=None,
            # Triangle/Square detection
            kernel_shape=None,
            approximation=None,
            max_area=None,
            # Colors detection by RGB
            red_min=None,
            green_min=None,
            blue_min=None,
            red_max=None,
            green_max=None,
            blue_max=None,
            # Colors detection by RGB
            hue_min=None,
            saturation_min=None,
            value_min=None,
            hue_max=None,
            saturation_max=None,
            value_max=None,
            # Face and eye cascades
            face_cascade=None,
            eye_cascade=None,
            # Face detection
            face_scale_factor=None,
            face_min_neighbors=None,
            face_min_size=None,
            face_max_size=None,
            # Eyes detection
            eye_scale_factor=None,
            eye_min_neighbors=None,
            eye_min_size=None,
            eye_max_size=None
    ):
        self.video = cv2.VideoCapture(0)
        self.shape_detection = shape_detection
        self.color_detection = color_detection
        self.face_detection = face_detection
        # Circle detection variables
        self.dp = dp
        self.min_dist = min_dist
        self.param1 = param1
        self.param2 = param2
        self.min_radius = min_radius
        self.max_radius = max_radius
        # Triangle/Square detection variables
        self.kernel_shape = kernel_shape
        self.approximation = approximation
        self.max_area = max_area
        # Color detection by RGB variables
        self.red_min = red_min
        self.green_min = green_min
        self.blue_min = blue_min
        self.red_max = red_max
        self.green_max = green_max
        self.blue_max = blue_max
        # Color detection by HSV variables
        self.hue_min = hue_min
        self.saturation_min = saturation_min
        self.value_min = value_min
        self.hue_max = hue_max
        self.saturation_max = saturation_max
        self.value_max = value_max
        # Face and eye cascade variables
        self.face_cascade = face_cascade
        self.eye_cascade = eye_cascade
        # Face detection variables
        self.face_scale_factor = face_scale_factor
        self.face_min_neighbors = face_min_neighbors
        self.face_min_size = face_min_size
        self.face_max_size = face_max_size
        # Eye detection variables
        self.eye_scale_factor = eye_scale_factor
        self.eye_min_neighbors = eye_min_neighbors
        self.eye_min_size = eye_min_size
        self.eye_max_size = eye_max_size

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
                                            minDist=self.min_dist,  # min distance between two circles centers
                                            param1=self.param1,
                                            param2=self.param2,
                                            minRadius=self.min_radius,
                                            maxRadius=self.max_radius)
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
        kernel = np.ones((self.kernel_shape, self.kernel_shape), np.uint8)
        erosion = cv2.erode(gray, kernel, iterations=1)
        dilation = cv2.dilate(erosion, kernel, iterations=1)
        blur = cv2.GaussianBlur(dilation, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def detect_triangles(self, image):
        for cnt in self.find_contours(image):
            area = cv2.contourArea(cnt)
            if area > self.max_area:
                epsilon = self.approximation * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                if len(approx) == 3:
                    cv2.drawContours(image, [approx], 0, (0, 255, 0), -1)

    def detect_squares(self, image):
        for cnt in self.find_contours(image):
            area = cv2.contourArea(cnt)
            if area > self.max_area:
                epsilon = self.approximation * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(approx)
                    circle_check = float(w) / h
                    if 0.95 <= circle_check < 1.05:
                        cv2.drawContours(image, [approx], 0, (0, 255, 0), -1)

    @staticmethod
    def count_hsv_values(hue, saturation, value):
        cv_hue = hue // 2
        cv_saturation = round(saturation * 2.55)
        cv_value = round(value * 2.55)

        return [cv_hue, cv_saturation, cv_value]

    def detect_color_by_hsv(self, image):
        # For HSV hue range is [0,179], saturation range is [0,255], and value range is [0,255].
        hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        given_min_hsv = self.count_hsv_values(self.hue_min, self.saturation_min, self.value_min)
        given_max_hsv = self.count_hsv_values(self.hue_max, self.saturation_max, self.value_max)
        low_range = np.array(given_min_hsv)
        high_range = np.array(given_max_hsv)
        mask = cv2.inRange(hsv_frame, low_range, high_range)
        output = cv2.bitwise_and(image, image, mask=mask)
        return output

    @staticmethod
    def convert_rgb_to_hsv(red, green, blue):
        bgr_color = np.uint8([[[blue, green, red]]])
        hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
        return hsv_color[0][0]

    def detect_color_by_rgb(self, image):
        # For RGB red, green and blue range is [0,255].
        hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        low_range = np.array(self.convert_rgb_to_hsv(self.red_min, self.green_min, self.blue_min))
        high_range = np.array(self.convert_rgb_to_hsv(self.red_max, self.green_max, self.blue_max))
        mask = cv2.inRange(hsv_frame, low_range, high_range)
        output = cv2.bitwise_and(image, image, mask=mask)
        return output

    def set_face_cascade(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def set_eye_cascade(self):
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    def detect_face(self, image):
        if self.face_cascade is None:
            self.set_face_cascade()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = self.face_cascade.detectMultiScale(image=gray,
                                                   scaleFactor=self.face_scale_factor,
                                                   minNeighbors=self.face_min_neighbors,
                                                   minSize=None if self.face_min_size is None else (
                                                       self.face_min_size, self.face_min_size),
                                                   maxSize=None if self.face_max_size is None else (
                                                       self.face_max_size, self.face_max_size))
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if self.face_detection == "eyes":
                self.detect_eyes(image, gray, x, y, w, h)

    def detect_eyes(self, image, gray_image, x, y, w, h):
        if self.face_cascade is None:
            self.set_face_cascade()
        if self.eye_cascade is None:
            self.set_eye_cascade()
        roi_gray = gray_image[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]
        eyes = self.eye_cascade.detectMultiScale(image=roi_gray,
                                                 scaleFactor=self.eye_scale_factor,
                                                 minNeighbors=self.eye_min_neighbors,
                                                 minSize=None if self.eye_min_size is None else (
                                                    self.eye_min_size, self.eye_min_size),
                                                 maxSize=None if self.eye_max_size is None else (
                                                    self.eye_max_size, self.eye_max_size))
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

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
        cam_check, frame = self.video.read()
        if cam_check:
            width = int(self.video.get(3)) * 2
            height = int(self.video.get(4))

            if self.shape_detection == "circle":
                processed = frame.copy()
                self.detect_circles(processed)

            elif self.shape_detection == "triangle":
                processed = frame.copy()
                self.detect_triangles(processed)

            elif self.shape_detection == "square":
                processed = frame.copy()
                self.detect_squares(processed)

            elif self.color_detection == "HSV":
                processed = self.detect_color_by_hsv(frame.copy())

            elif self.color_detection == "RGB":
                processed = self.detect_color_by_rgb(frame.copy())

            elif self.face_detection == "face" or self.face_detection == "eyes":
                processed = frame.copy()
                self.detect_face(processed)
            else:
                processed = frame.copy()

            output = np.zeros((height, width, frame.shape[2]), np.uint8)
            output[:height, :width // 2] = frame
            output[:height, width // 2:] = processed

            # getting texts sizes

            input_text_w, input_text_h = VideoCamera.get_text_size('INPUT')
            output_text_w, output_text_h = VideoCamera.get_text_size('OUTPUT')

            # displaying texts backgrounds

            VideoCamera.display_text(output, 'INPUT', (0, 0), input_text_w, input_text_h)
            VideoCamera.display_text(output, 'OUTPUT', (width // 2, 0), output_text_w, output_text_h)

            # extract image to .jpg format
            _, jpeg = cv2.imencode('.jpg', output)

            return jpeg.tobytes()
        else:
            return 0

def gen(camera):
    if camera.get_frame() != 0:
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    else:
        return 0
