from .models import Task, Rights
from typing import List
from django.contrib.auth.models import User


# Get all tasks for user
def get_tasks(user: User) -> List[Task]:
    tasks = []
    for task in Task.objects.filter(user=user,
            completed=False).order_by('-created_at'):
        rights = Rights.objects.filter(task=task)
        tasks.append({
            'task': task,
            'rights': rights
        })

    completed = []
    for task in Task.objects.filter(user=user,
            completed=True).order_by('-completed_at'):
        rights = Rights.objects.filter(task=task)
        completed.append({
            'task': task,
            'rights': rights
        })

    # Get users for adding rights
    users = User.objects.exclude(username=user.username).all()
    
    rights = Rights.objects.filter(user=user)
    user_rights = {}

    for right in rights:
        un = right.task.user.username
        if un in user_rights:
            user_rights[un].append(right)
        else:
            user_rights[un] = [right]

    context = {
        'tasks': tasks,
        'completed': completed,
        'users': users,
        'rights': user_rights
    }
    return context


# Add right to user
def add_right(task: Task, username: str, can_edit: bool, can_view: bool):
    try:
        user = User.objects.get(username=username)
        Rights.objects.create(task=task, user=user, can_edit=can_edit, can_view=can_view)
    except User.DoesNotExist:
        return False

    if not can_view:
        Rights.objects.filter(user=user, task=task).delete()
        return True

    right = Rights.objects.update_or_create(
        user=user,
        task=task,
        defaults={'can_view': True, 'can_edit': can_edit}
    )
    right[0].save()
    return right[1]
