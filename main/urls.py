from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_task/', views.add_task, name='add_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('add_rights/<int:task_id>/', views.add_rights, name='add_rights'),
]
