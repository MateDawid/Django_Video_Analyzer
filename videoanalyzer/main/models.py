from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CircleDetectionModel(models.Model):
    dp = models.FloatField(default=1)
    minDist = models.FloatField(default=20)
    param1 = models.FloatField(default=50)
    param2 = models.FloatField(default=70)
    minRadius = models.IntegerField(default=20)
    maxRadius = models.IntegerField(default=100)


class TriangleAndSquareDetectionModel(models.Model):
    kernelShape = models.PositiveIntegerField(default=4)
    approximation = models.FloatField(default=0.02)
    maxArea = models.FloatField(default=400)


class ColorHSVDetectionModel(models.Model):
    min_hue = models.PositiveIntegerField(default=80, validators=[MaxValueValidator(359), MinValueValidator(0)])
    min_saturation = models.PositiveIntegerField(default=20, validators=[MaxValueValidator(255), MinValueValidator(0)])
    min_value = models.PositiveIntegerField(default=20, validators=[MaxValueValidator(255), MinValueValidator(0)])
    max_hue = models.PositiveIntegerField(default=160, validators=[MaxValueValidator(359), MinValueValidator(0)])
    max_saturation = models.PositiveIntegerField(default=100, validators=[MaxValueValidator(255), MinValueValidator(0)])
    max_value = models.PositiveIntegerField(default=100, validators=[MaxValueValidator(255), MinValueValidator(0)])
