# Generated by Django 3.2.2 on 2021-05-11 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20210507_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facedetectionmodel',
            name='face_scale_factor',
            field=models.FloatField(default=1.05, help_text='Help text'),
        ),
    ]