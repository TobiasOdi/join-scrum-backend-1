from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    color = models.CharField(max_length=25, blank=False, default=None)
    phone = models.CharField(max_length=25, blank=True, default=None)
    
    def __str__(self):
        return self.color
    