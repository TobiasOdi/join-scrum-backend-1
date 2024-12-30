from add_task.models import TaskItem

def createNewTask(taskData, request):
    return TaskItem.objects.create(
        category=taskData[0]['category'], 
        created_by=request.user,
        description=taskData[0]['description'],
        due_date=taskData[0]['due_date'],
        priorityValue=taskData[0]['priorityValue'],
        statusCategory=taskData[0]['statusCategory'],
        title=taskData[0]['title']
        )