# Generated by Django 2.1.7 on 2019-03-27 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_newreservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newreservation',
            name='guest',
        ),
        migrations.RemoveField(
            model_name='newreservation',
            name='table',
        ),
        migrations.DeleteModel(
            name='NewReservation',
        ),
    ]
