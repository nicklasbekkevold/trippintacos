from django.db import models
from guest.models import Guest
# Create your models here.


class Employee(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        app_label = 'emlpoyee'
