from django.db import models

# Create your models here.


class Guest(models.Model):
    email = models.EmailField()
    reminder = models.BooleanField()
