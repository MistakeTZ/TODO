from .models import Task, Rights
from typing import List
from django.contrib.auth.models import User


def get_tasks(user: User) -> List[Task]:
    return Task.objects.filter(user=user)
