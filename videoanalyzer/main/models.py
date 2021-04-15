from django.db import models

# DISPLAY_MODES = (
#     ('clean', 'Clean'),
#     ('shape', 'Shape'),
#     ('color', 'Color'),
#     ('color_and_shape', 'Color + Shape'),
#     ('face', 'Face')
# )
#
#
# class DisplayModel(models.Model):
#     display_mode = models.CharField(max_length=20, choices=DISPLAY_MODES, default='clean')


class CircleDetectionModel(models.Model):
    dp = models.FloatField(default=1)
    minDist = models.FloatField(default=20)
    param1 = models.FloatField(default=50)
    param2 = models.FloatField(default=70)
    minRadius = models.IntegerField(default=20)
    maxRadius = models.IntegerField(default=100)


class TriangleDetectionModel(models.Model):
    kernelShape = models.IntegerField(default=4)
    approximation = models.FloatField(default=0.02)
    maxArea = models.FloatField(default=400)
