from django.shortcuts import render
import json
from rest_framework.views import APIView, Response# Create your views here.
from add_task.models import TaskItem, AssignedContactItem, SubtaskItem
from contacts.models import ContactItem
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication

class SaveTaskCategoryView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, task_id):
        currentTask = json.loads(request.body)
        #print("JSON", currentTask['id'])
        TaskItem.objects.filter(pk=task_id).update(
            statusCategory=currentTask['statusCategory'],
        )      
        return Response({ "status": "OK - Status category updated"})

class DeleteTaskView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, task_id):
        #currentTask = json.loads(request.body)      
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

        TaskItem.objects.filter(pk=task_id).update(
            category=taskData[0]['category'], 
            description=taskData[0]['description'],
            due_date=taskData[0]['due_date'],
            priorityValue=taskData[0]['priorityValue'],
            statusCategory=taskData[0]['statusCategory'],
            title=taskData[0]['title']
        )  
        
        # DELETE ALL SUBTASKS AND ASSIGNED CONTACTS THAT REFER TO THE CURRENT TASK
        SubtaskItem.objects.filter(parent_task_id=get_current_Task[0]).delete()
        AssignedContactItem.objects.filter(parent_task_id=get_current_Task[0]).delete()

        # ADD NEW SUBTASKS AND ASSIGNED CONTACTS
        for subtask in subtaskData: 
            SubtaskItem.objects.create(
                parent_task_id=get_current_Task[0],
                status=subtask['status'], 
                subtaskName=subtask['subtaskName']
            )

        for assignedContact in assignedToData:
            current_contact = ContactItem.objects.filter(pk=assignedContact['contact_id'])
            
            AssignedContactItem.objects.create(
                parent_task_id=get_current_Task[0],
                contact_id=current_contact[0]
            )  
        return Response({ "status": "OK - Task edited"})
