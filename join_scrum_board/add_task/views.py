from django.shortcuts import render
from add_task.models import CategoryItem
from rest_framework.views import APIView, Response
from add_task.models import TaskItem, AssignedContactItem, SubtaskItem
from contacts.models import ContactItem
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core import serializers
from rest_framework.authentication import TokenAuthentication

  
class SaveCreatedTaskView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        currentTask = json.loads(request.body)      
        taskData = currentTask[0]['taskData']
        subtaskData = currentTask[0]['subtaskData']
        assignedToData = currentTask[0]['assignedToData']
        newTask = TaskItem.objects.create(
            category=taskData[0]['category'], 
            created_by=request.user,
            description=taskData[0]['description'],
            due_date=taskData[0]['due_date'],
            priorityValue=taskData[0]['priorityValue'],
            statusCategory=taskData[0]['statusCategory'],
            title=taskData[0]['title']
            )

        for subtask in subtaskData: 
            SubtaskItem.objects.create(
                parent_task_id=newTask,
                status=subtask['status'], 
                subtaskName=subtask['subtaskName']
            )

        for assignedContact in assignedToData:
            contactId = ContactItem.objects.filter(id=assignedContact)     
            AssignedContactItem.objects.create(
                parent_task_id=newTask,
                contact_id=contactId[0]
            )

        return Response({ "status": "OK - New task created"})

class SaveCreatedCategoryView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        newCategory = json.loads(request.body)
        
        CategoryItem.objects.create(
            categoryName=newCategory['categoryName'], 
            color=newCategory['color'],
            categoryType=newCategory['categoryType'],
        )  
        
        return Response({ "status": "OK - Category created"})

class DeleteCategoryView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        currentCategory = json.loads(request.body)        
        CategoryItem.objects.filter(id=currentCategory['id']).delete()
        return Response({ "status": "OK - Catgory deleted"})