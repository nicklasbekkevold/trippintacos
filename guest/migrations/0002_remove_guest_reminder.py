# Generated by Django 2.1.7 on 2019-02-28 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='reminder',
        ),
    ]
