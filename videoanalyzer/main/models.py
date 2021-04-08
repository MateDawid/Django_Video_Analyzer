from django.db import models

DISPLAY_MODES = (
    ('clean', 'clean'),
    ('shape', 'shape'),
    ('color', 'color'),
    ('face', 'face')
)


class DisplayModel(models.Model):
    display_mode = models.CharField(max_length=6, choices=DISPLAY_MODES, default='clean')
