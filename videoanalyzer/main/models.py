from django.db import models

DISPLAY_MODES = (
    ('clean', 'Clean'),
    ('shape', 'Shape'),
    ('color', 'Color'),
    ('color_and_shape', 'Color + Shape'),
    ('face', 'Face')
)


class DisplayModel(models.Model):
    display_mode = models.CharField(max_length=20, choices=DISPLAY_MODES, default='clean')
