from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .models import Task, Rights
from .tasks import get_tasks, add_right


def index(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        context = get_tasks(request.user)
        return render(request, 'main/index.html', context)
    else:
        return redirect('login')


def add_task(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', None)

        if title:
            task = Task(user=request.user, title=title, description=description)
            task.save()
    
    return redirect('index')


def edit_task(request: HttpRequest, task_id: int) -> HttpResponse:
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        if task.user != request.user:
            if not Rights.objects.filter(user=request.user,
                        task=task, can_edit=True).exists():
                return redirect('index')

        if 'delete' in request.POST:
            if task.user == request.user:
                task.delete()
            return redirect('index')

        title = request.POST.get('title')
        if title:
            task.title = title
            task.save()

        completed = request.POST.get('completed', 'False')
        if completed:
            task.completed = completed == 'True'
            task.save()

    return redirect('index')


def add_rights(request: HttpRequest, task_id: int) -> HttpResponse:
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        if task.user != request.user:
            return redirect('index')

        add_right(task, request.POST.get('user'),
                   request.POST.get('can_edit', 'False') == 'True',
                   request.POST.get('can_view', 'False') == 'True')

    return redirect('index')
