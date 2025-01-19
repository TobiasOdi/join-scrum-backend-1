from django.shortcuts import render
import json
from rest_framework.views import APIView, Response
from add_task_app.models import TaskItem, AssignedContactItem, SubtaskItem, CategoryItem
from rest_framework.authentication import TokenAuthentication
from board_app.helpers import *
from contacts_app.models import ContactItem
from add_task_app.api.serializers import TaskItemSerializer, SubtaskItemSerializer, AssignedContactItemSerializer, CategoryItemSerializer
from contacts_app.api.serializers import ContactItemSerializer

class DataView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def get(self, request, format=None):
        """ Gets all entries from the tasks table, subtask table, assigned contacts table, contacts table and categories table.
        Returns a JSON with all the database data.
        """
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

class SetCategoriesView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        """ At the first login, all task categories are being created (categories table).
        Returns a string that says "OK - Categories created and saved in database".
        """
        categories = json.loads(request.body)      

        for category in categories: 
            CategoryItem.objects.create(
                categoryName = category['categoryName'],
                color = category['color'],
                categoryType = category['categoryType']
            )
        return Response({ "status": "OK - Categories created and saved in database"})

class SaveTaskCategoryView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, task_id):
        """ Updates the status category of the task.
        Args:
            request (json): Task data
            task_id (int): Id of the tasks updated status category
        Returns a string that says "OK - Status category updated".
        """
        currentTask = json.loads(request.body)
        TaskItem.objects.filter(pk=task_id).update(
            statusCategory=currentTask['statusCategory'],
        )      
        return Response({ "status": "OK - Status category updated"})

class DeleteTaskView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, task_id):
        """ Deletes the task item form the database.
        Args:
            task_id (int): _description_
        Returns a string that says "OK - Task deleted".
        """
        TaskItem.objects.filter(id=task_id).delete()
        return Response({ "status": "OK - Task deleted"})

class SaveSubtaskStatus(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, subtask_id):
        """ Saves the stauts (done/undone) of the current subtask.
        Args:
            request (json): _description_
            subtask_id (int): Id of the changed subtask
        Returns a string that says "OK - Subtask status changed".
        """
        currentSubtask = json.loads(request.body)      
        SubtaskItem.objects.filter(id=subtask_id).update(
            status=currentSubtask['status'], 
        ) 
        return Response({ "status": "OK - Subtask status changed"})

class SaveEditedTaskView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, task_id):
        """ Saves the update task data to the database.
        Args:
            request (json): Task data
            task_id (int): Id of the updated task
        Returns a string that says "OK - Task edited".
        """
        currentTask = json.loads(request.body)        
        taskData = currentTask[0]['taskData']
        subtaskData = currentTask[0]['subtaskData']
        assignedToData = currentTask[0]['assignedToData']
        get_current_Task=TaskItem.objects.filter(pk=task_id)
        
        updateTaskItem(task_id, taskData)
        SubtaskItem.objects.filter(parent_task_id=get_current_Task[0]).delete()
        AssignedContactItem.objects.filter(parent_task_id=get_current_Task[0]).delete()
        createSubtasks(subtaskData, get_current_Task)
        createAssignedContacts(assignedToData, get_current_Task)
        return Response({ "status": "OK - Task edited"})
