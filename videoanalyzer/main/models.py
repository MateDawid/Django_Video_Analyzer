from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CircleDetectionModel(models.Model):
    dp = models.FloatField(default=1)
    min_dist = models.FloatField(default=20)
    param1 = models.FloatField(default=50)
    param2 = models.FloatField(default=70)
    min_radius = models.IntegerField(default=20)
    max_radius = models.IntegerField(default=100)


class TriangleAndSquareDetectionModel(models.Model):
    kernel_shape = models.PositiveIntegerField(default=4)
    approximation = models.FloatField(default=0.02)
    max_area = models.FloatField(default=400)


class ColorHSVDetectionModel(models.Model):
    min_hue = models.PositiveIntegerField(default=80, validators=[MaxValueValidator(359), MinValueValidator(0)])
    min_saturation = models.PositiveIntegerField(default=20, validators=[MaxValueValidator(255), MinValueValidator(0)])
    min_value = models.PositiveIntegerField(default=20, validators=[MaxValueValidator(255), MinValueValidator(0)])
    max_hue = models.PositiveIntegerField(default=160, validators=[MaxValueValidator(359), MinValueValidator(0)])
    max_saturation = models.PositiveIntegerField(default=100, validators=[MaxValueValidator(255), MinValueValidator(0)])
    max_value = models.PositiveIntegerField(default=100, validators=[MaxValueValidator(255), MinValueValidator(0)])


class ColorRGBDetectionModel(models.Model):
    red_min = models.PositiveIntegerField(default=48, validators=[MaxValueValidator(255), MinValueValidator(0)])
    green_min = models.PositiveIntegerField(default=51, validators=[MaxValueValidator(255), MinValueValidator(0)])
    blue_min = models.PositiveIntegerField(default=41, validators=[MaxValueValidator(255), MinValueValidator(0)])
    red_max = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(255), MinValueValidator(0)])
    green_max = models.PositiveIntegerField(default=255, validators=[MaxValueValidator(255), MinValueValidator(0)])
    blue_max = models.PositiveIntegerField(default=171, validators=[MaxValueValidator(255), MinValueValidator(0)])


class FaceDetectionModel(models.Model):
    face_scale_factor = models.FloatField(default=1.05)
    face_min_neighbors = models.PositiveIntegerField(default=6)
    face_min_size = models.PositiveIntegerField(default=100, null=True, blank=True)
    face_max_size = models.PositiveIntegerField(null=True, blank=True)


class EyesDetectionModel(FaceDetectionModel):
    eye_scale_factor = models.FloatField(default=1.3)
    eye_min_neighbors = models.PositiveIntegerField(default=5)
    eye_min_size = models.PositiveIntegerField(null=True, blank=True)
    eye_max_size = models.PositiveIntegerField(null=True, blank=True)
