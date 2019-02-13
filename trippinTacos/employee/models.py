from django.db import models
from guest.models import Guest
# Create your models here.


class Emlpoyee(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    