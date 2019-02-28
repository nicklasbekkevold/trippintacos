from django.db import models

# Create your models here.


class Guest(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    def __str__(self):
        return str(self.email)

    class Meta:
        app_label = 'guest'