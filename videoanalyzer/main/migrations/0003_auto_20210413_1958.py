# Generated by Django 3.1.7 on 2021-04-13 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210413_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circledetectionmodel',
            name='dp',
            field=models.FloatField(default=1),
        ),
    ]
