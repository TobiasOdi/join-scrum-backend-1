from django.shortcuts import render
from add_task.models import CategoryItem
from rest_framework.views import APIView, Response
from add_task.models import AssignedContactItem, SubtaskItem
from contacts.models import ContactItem
import json
from rest_framework.authentication import TokenAuthentication
from add_task.helpers import *

  
class SaveCreatedTaskView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        currentTask = json.loads(request.body)      
        taskData = currentTask[0]['taskData']
        subtaskData = currentTask[0]['subtaskData']
        assignedToData = currentTask[0]['assignedToData']
        newTask = createNewTask(taskData, request)      
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
    def post(self, request, category_id):
        CategoryItem.objects.filter(id=category_id).delete()
        return Response({ "status": "OK - Catgory deleted"})