from django.db import models
from django.conf import settings
from django.db.models.fields import DateField
from datetime import date
from contacts_app.models import ContactItem

# Create your models here.
class TaskItem(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = DateField(default=date.today)
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=25)
    due_date = models.DateField()
    priorityValue = models.CharField(max_length=10)
    statusCategory = models.CharField(max_length=25)
    
    def __str__(self):
        return f"{self.id} {self.title}"

class SubtaskItem(models.Model):
    parent_task_id = models.ForeignKey(TaskItem, on_delete=models.CASCADE, default=None)
    subtaskName = models.CharField(max_length=50)
    status = models.CharField(max_length=6)
    
    def __str__(self):
        return f"{self.parent_task_id} {self.subtaskName}"

class AssignedContactItem(models.Model):
    parent_task_id = models.ForeignKey(TaskItem, on_delete=models.CASCADE, default=None)
    contact_id = models.ForeignKey(ContactItem, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return f"{self.parent_task_id} {self.contact_id}"
    
class CategoryItem(models.Model):
    categoryName = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
    categoryType = models.CharField(max_length=25)
    
    def __str__(self):
        return f"{self.categoryName}"
