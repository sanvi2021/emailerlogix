# Generated by Django 4.1.2 on 2022-10-12 13:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_appreport_record_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appreport',
            name='record_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 12, 18, 41, 32, 516329)),
        ),
    ]
