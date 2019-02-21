from django.db import models

# Create your models here.


class Guest(models.Model):
    email = models.EmailField()
    reminder = models.BooleanField()

    def __str__(self):
        return self.email

    class Meta:
        app_label = "guest"
