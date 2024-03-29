# Generated by Django 2.1.7 on 2019-03-27 10:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('guest', '0003_merge_20190327_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_people', models.IntegerField(default=0)),
                ('start_date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('walkin', models.BooleanField(default=False)),
                ('reminder', models.BooleanField(blank=True, null=True)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guest.Guest')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250)),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_seats', models.IntegerField()),
                ('is_occupied', models.BooleanField(default=False)),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservations.Restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservations.Table'),
        ),
    ]
