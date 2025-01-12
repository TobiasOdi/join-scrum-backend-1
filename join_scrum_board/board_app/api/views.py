from django.shortcuts import render
import json
from rest_framework.views import APIView, Response
from add_task_app.models import TaskItem, AssignedContactItem, SubtaskItem, CategoryItem
from rest_framework.authentication import TokenAuthentication
from board_app.api.helpers import *
from contacts_app.models import ContactItem
from add_task_app.api.serializers import TaskItemSerializer, SubtaskItemSerializer, AssignedContactItemSerializer, CategoryItemSerializer
from contacts_app.api.serializers import ContactItemSerializer

class DataView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def get(self, request, format=None):
        tasks = TaskItem.objects.all()
        task_serializer = TaskItemSerializer(tasks, many=True)
        subtasks = SubtaskItem.objects.all()
        subtasks_serializer = SubtaskItemSerializer(subtasks, many=True)
        assignedContacts = AssignedContactItem.objects.all()
        assignedContacts_serializer = AssignedContactItemSerializer(assignedContacts, many=True)
        contacts = ContactItem.objects.all()
        contacts_serializer = ContactItemSerializer(contacts, many=True)
        categories = CategoryItem.objects.all()
        categories_serializer = CategoryItemSerializer(categories, many=True)       
        return Response(
            {
                'tasks': task_serializer.data,
                'subtasks': subtasks_serializer.data,
                'assignedContacts': assignedContacts_serializer.data,
                'contacts': contacts_serializer.data,
                'categories': categories_serializer.data
            })       

""" class CategoriesView(APIView): 
    authenticaiton_classes = [TokenAuthentication]
    def get(self, request, format=None):
        categories = CategoryItem.objects.all()
        serializer = CategoryItemSerializer(categories, many=True)
        return Response(serializer.data) 
"""  

class SetCategoriesView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        categories = json.loads(request.body)      

        for category in categories: 
            CategoryItem.objects.create(
                categoryName = category['categoryName'],
                color = category['color'],
                categoryType = category['categoryType']
            )
        return Response({ "status": "OK - Categories saved in database"})

class SaveTaskCategoryView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, task_id):
        currentTask = json.loads(request.body)
        TaskItem.objects.filter(pk=task_id).update(
            statusCategory=currentTask['statusCategory'],
        )      
        return Response({ "status": "OK - Status category updated"})

class DeleteTaskView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, task_id):
        TaskItem.objects.filter(id=task_id).delete()
        return Response({ "status": "OK - Task deleted"})

class SaveSubtaskStatus(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, subtask_id):
        currentSubtask = json.loads(request.body)      
        SubtaskItem.objects.filter(id=subtask_id).update(
            status=currentSubtask['status'], 
        ) 
        return Response({ "status": "OK - Subtask status changed"})

class SaveEditedTaskView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, task_id):
        currentTask = json.loads(request.body)        
        taskData = currentTask[0]['taskData']
        subtaskData = currentTask[0]['subtaskData']
        assignedToData = currentTask[0]['assignedToData']
        get_current_Task=TaskItem.objects.filter(pk=task_id)
        
        #Update the task item
        updateTaskItem(task_id, taskData)
        # DELETE ALL SUBTASKS AND ASSIGNED CONTACTS THAT REFER TO THE CURRENT TASK
        SubtaskItem.objects.filter(parent_task_id=get_current_Task[0]).delete()
        AssignedContactItem.objects.filter(parent_task_id=get_current_Task[0]).delete()
        # ADD NEW SUBTASKS AND ASSIGNED CONTACTS
        createSubtasks(subtaskData, get_current_Task)
        createAssignedContacts(assignedToData, get_current_Task)
        
        return Response({ "status": "OK - Task edited"})
