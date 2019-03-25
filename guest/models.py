from django.db import models

# Create your models here.


class Guest(models.Model):
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    # agreed_terms = models.BooleanField(null=False, default=False)

    def __str__(self):
        return str(self.email)

    class Meta:
        app_label = 'guest'
