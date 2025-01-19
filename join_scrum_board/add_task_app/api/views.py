from django.shortcuts import render
from add_task_app.models import CategoryItem, AssignedContactItem, SubtaskItem
from rest_framework.views import APIView, Response
from contacts_app.models import ContactItem
import json
from rest_framework.authentication import TokenAuthentication
from add_task_app.helpers import *


  
class SaveCreatedTaskView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        """ Takes the json data and creates a new task item, subtask item and contact item in the database.
        Args:
            request (json): Task data, subtask data, assigned contact data
        Returns a string that says "OK - New task created".
        """
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
        """ Takes the json data and creates a new category item in the database.
        Args:
            request (json): Category data
        Returns a string that says "OK - Category created".
        """
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
        """ Deletes a cutom made category.
        Args:
            category_id (int): Id of the category to be deleted.

        Returns a string that says "OK - Category deleted".
        """
        CategoryItem.objects.filter(id=category_id).delete()
        return Response({ "status": "OK - Catgory deleted"})