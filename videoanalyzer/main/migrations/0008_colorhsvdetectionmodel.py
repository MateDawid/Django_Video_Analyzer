# Generated by Django 3.1.7 on 2021-04-28 19:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210422_1935'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorHSVDetectionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_hue', models.IntegerField(default=80, validators=[django.core.validators.MaxValueValidator(179), django.core.validators.MinValueValidator(0)])),
                ('min_saturation', models.IntegerField(default=20, validators=[django.core.validators.MaxValueValidator(255), django.core.validators.MinValueValidator(0)])),
                ('min_value', models.IntegerField(default=20, validators=[django.core.validators.MaxValueValidator(255), django.core.validators.MinValueValidator(0)])),
                ('max_hue', models.IntegerField(default=160, validators=[django.core.validators.MaxValueValidator(179), django.core.validators.MinValueValidator(0)])),
                ('max_saturation', models.IntegerField(default=100, validators=[django.core.validators.MaxValueValidator(255), django.core.validators.MinValueValidator(0)])),
                ('max_value', models.IntegerField(default=100, validators=[django.core.validators.MaxValueValidator(255), django.core.validators.MinValueValidator(0)])),
            ],
        ),
    ]