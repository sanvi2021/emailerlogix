# Generated by Django 4.1.2 on 2022-10-10 17:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_appreport_record_time_rdmstr'),
    ]

    operations = [
        migrations.AddField(
            model_name='appreport',
            name='label',
            field=models.CharField(default='Inbox', max_length=20),
        ),
        migrations.AlterField(
            model_name='appreport',
            name='record_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 10, 23, 2, 5, 38951)),
        ),
    ]