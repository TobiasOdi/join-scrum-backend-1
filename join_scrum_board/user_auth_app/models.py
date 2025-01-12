from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    color = models.CharField(max_length=25, blank=False, default=None)
    text_color = models.CharField(max_length=25, blank=False, default=None)
    phone = models.CharField(max_length=25, blank=True, default=None)
    
    def __str__(self):
        return self.color
    
class PwResetTimestamp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.IntegerField(default=0)    
    
    def __str__(self):
        return str(self.timestamp)