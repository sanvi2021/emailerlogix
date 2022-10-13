# Generated by Django 4.1.2 on 2022-10-11 09:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_appreport_record_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appreport',
            name='DMARC_record',
            field=models.CharField(default='Pass', max_length=10),
        ),
        migrations.AlterField(
            model_name='appreport',
            name='dkim_record',
            field=models.CharField(default='Pass', max_length=10),
        ),
        migrations.AlterField(
            model_name='appreport',
            name='record_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 11, 15, 5, 5, 596779)),
        ),
        migrations.AlterField(
            model_name='appreport',
            name='spf_record',
            field=models.CharField(default='Pass', max_length=10),
        ),
    ]
