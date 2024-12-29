from django.shortcuts import render
import json
from rest_framework.views import APIView, Response
from add_task.models import TaskItem, AssignedContactItem, SubtaskItem
from rest_framework.authentication import TokenAuthentication
from board.helpers import *

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
