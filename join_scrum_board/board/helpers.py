from add_task.models import TaskItem, AssignedContactItem, SubtaskItem
from contacts.models import ContactItem

def updateTaskItem(task_id, taskData):
    TaskItem.objects.filter(pk=task_id).update(
        category=taskData[0]['category'], 
        description=taskData[0]['description'],
        due_date=taskData[0]['due_date'],
        priorityValue=taskData[0]['priorityValue'],
        statusCategory=taskData[0]['statusCategory'],
        title=taskData[0]['title']
    ) 
            
def createSubtasks(subtaskData, get_current_Task):
    for subtask in subtaskData: 
        SubtaskItem.objects.create(
            parent_task_id=get_current_Task[0],
            status=subtask['status'], 
            subtaskName=subtask['subtaskName']
        )
        
def createAssignedContacts(assignedToData, get_current_Task):
    for assignedContact in assignedToData:
        current_contact = ContactItem.objects.filter(pk=assignedContact['contact_id'])
        AssignedContactItem.objects.create(
            parent_task_id=get_current_Task[0],
            contact_id=current_contact[0]
        )          
