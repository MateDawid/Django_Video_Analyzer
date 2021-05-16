from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CircleDetectionModel(models.Model):
    dp = models.FloatField(verbose_name="DP", default=1, help_text="Inverse resolution ratio.")
    min_dist = models.FloatField(verbose_name="MIN_DIST", default=20, help_text="Minimum distance between detected centers.")
    param1 = models.FloatField(verbose_name="PARAM1", default=50, help_text="Upper threshold for the internal Canny edge detector.")
    param2 = models.FloatField(verbose_name="PARAM2", default=70, help_text="Threshold for center detection.")
    min_radius = models.IntegerField(verbose_name="MIN_RADIUS", default=20, help_text="Minimum radius to be detected.")
    max_radius = models.IntegerField(verbose_name="MAX_RADIUS", default=100, help_text="Maximum radius to be detected.")


class TriangleAndSquareDetectionModel(models.Model):
    kernel_shape = models.PositiveIntegerField(verbose_name="KERNEL SHAPE", default=4, help_text="The number of columns and rows of ones in the numpy array.")
    approximation = models.FloatField(verbose_name="APPROXIMATION", default=0.02, help_text="Approximation of detected shape.")
    max_area = models.FloatField(verbose_name="MAX AREA", default=400, help_text="Maximum area of detected shape.")


class ColorHSVDetectionModel(models.Model):
    min_hue = models.PositiveIntegerField(verbose_name="HUE MIN", default=80, validators=[MaxValueValidator(359), MinValueValidator(0)], help_text="Minimum hue (0 - 360).")
    min_saturation = models.PositiveIntegerField(verbose_name="SATURATION MIN", default=20, validators=[MaxValueValidator(100), MinValueValidator(0)], help_text="Minimum saturation (0 - 100).")
    min_value = models.PositiveIntegerField(verbose_name="VALUE MIN", default=20, validators=[MaxValueValidator(100), MinValueValidator(0)], help_text="Minimum value (0 - 100).")
    max_hue = models.PositiveIntegerField(verbose_name="HUE MAX", default=160, validators=[MaxValueValidator(359), MinValueValidator(0)], help_text="Maximum hue (0 - 360).")
    max_saturation = models.PositiveIntegerField(verbose_name="SATURATION MAX", default=100, validators=[MaxValueValidator(100), MinValueValidator(0)], help_text="Maximum hue (0 - 100).")
    max_value = models.PositiveIntegerField(verbose_name="VALUE MAX", default=100, validators=[MaxValueValidator(100), MinValueValidator(0)], help_text="Maximum value (0 - 100).")


class ColorRGBDetectionModel(models.Model):
    red_min = models.PositiveIntegerField(verbose_name="RED MIN", default=48, validators=[MaxValueValidator(255), MinValueValidator(0)], help_text="Minimum red value (0 - 255).")
    green_min = models.PositiveIntegerField(verbose_name="GREEN MIN", default=51, validators=[MaxValueValidator(255), MinValueValidator(0)], help_text="Minimum green value (0 - 255).")
    blue_min = models.PositiveIntegerField(verbose_name="BLUE MIN", default=41, validators=[MaxValueValidator(255), MinValueValidator(0)], help_text="Minimum blue value (0 - 255).")
    red_max = models.PositiveIntegerField(verbose_name="RED MAX", default=0, validators=[MaxValueValidator(255), MinValueValidator(0)], help_text="Maximum red value (0 - 255).")
    green_max = models.PositiveIntegerField(verbose_name="GREEN MAX", default=255, validators=[MaxValueValidator(255), MinValueValidator(0)], help_text="Maximum green value (0 - 255).")
    blue_max = models.PositiveIntegerField(verbose_name="BLUE MAX", default=171, validators=[MaxValueValidator(255), MinValueValidator(0)], help_text="Maximum blue value (0 - 255).")


class FaceDetectionModel(models.Model):
    face_scale_factor = models.FloatField(verbose_name='FACE SCALE FACTOR', default=1.05, help_text='Specifies how much the image size is reduced at each image scale.')
    face_min_neighbors = models.PositiveIntegerField(verbose_name="FACE MIN NEIGHBORS", default=6, help_text='Specifies how many neighbors each candidate rectangle should have to retain it.')
    face_min_size = models.PositiveIntegerField(verbose_name="FACE MIN SIZE", default=100, null=True, blank=True, help_text='Minimum possible object size.')
    face_max_size = models.PositiveIntegerField(verbose_name="FACE MAX SIZE", null=True, blank=True, help_text='Maximum possible object size.')


class EyesDetectionModel(FaceDetectionModel):
    eye_scale_factor = models.FloatField(verbose_name='EYE SCALE FACTOR', default=1.3, help_text='Specifies how much the image size is reduced at each image scale.')
    eye_min_neighbors = models.PositiveIntegerField(verbose_name="EYE MIN NEIGHBORS", default=5, help_text='Specifies how many neighbors each candidate rectangle should have to retain it.')
    eye_min_size = models.PositiveIntegerField(verbose_name="EYE MIN SIZE", null=True, blank=True, help_text='Minimum possible object size.')
    eye_max_size = models.PositiveIntegerField(verbose_name="EYE MAX SIZE", null=True, blank=True, help_text='Maximum possible object size.')
