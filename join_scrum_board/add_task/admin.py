from django.contrib import admin
from add_task.models import TaskItem, SubtaskItem, CategoryItem, AssignedContactItem

# Register your models here.
admin.site.register(TaskItem)
admin.site.register(SubtaskItem)
admin.site.register(CategoryItem)
admin.site.register(AssignedContactItem)