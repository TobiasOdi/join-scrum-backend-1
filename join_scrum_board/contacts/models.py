from django.db import models
from django.conf import settings
from django.db.models.fields import DateField
from datetime import date

# Create your models here.
class ContactItem(models.Model):
    active_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    phone = models.CharField(max_length=25)
    color = models.CharField(max_length=25)

    def __str__(self):
        return f"({self.id})"
