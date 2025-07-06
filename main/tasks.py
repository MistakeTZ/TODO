from .models import Task, Rights
from typing import List
from django.contrib.auth.models import User


def get_tasks(user: User) -> List[Task]:
    tasks = Task.objects.filter(user=user,
                        completed=False).order_by('-created_at')
    completed = Task.objects.filter(user=user,
                    completed=True).order_by('-completed_at')

    context = {
        'tasks': tasks,
        'completed': completed
    }
    return context
