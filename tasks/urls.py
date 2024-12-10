from django.urls import path
from . import views
from .authentication import UserRegisterView, UserLoginView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('tasks/', views.create_task, name='create-task'),
    path('get-tasks/', views.view_tasks, name='view-tasks'),
    path('tasks/<int:pk>/', views.delete_task, name='delete-task'),
]
