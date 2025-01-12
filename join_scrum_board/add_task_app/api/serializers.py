from add_task_app.models import TaskItem, SubtaskItem, CategoryItem, AssignedContactItem
from user_auth_app.models import UserAccount
from django.contrib.auth.models import User
from rest_framework import serializers

class TaskItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskItem
        fields = "__all__"

class SubtaskItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtaskItem
        fields = "__all__"
     
class AssignedContactItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignedContactItem
        fields = "__all__"

class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryItem
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email']

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['user', 'color', 'phone']
