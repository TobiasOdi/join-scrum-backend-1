from django.db import models
from django.conf import settings
from datetime import date

# Create your models here.
class ContactItem(models.Model):
    active_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    phone = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
    text_color = models.CharField(max_length=25, null=True)

    def __str__(self):
        return f"({self.id})"
