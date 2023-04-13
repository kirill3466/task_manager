from django.urls import path
from .views import TaskList, TaskCreate, TaskDelete,  logoutUser, LoginUser, RegisterUser, detail

urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('today-tasks', TaskList.as_view(), name='today-tasks'),
    path('last-3-days-tasks', TaskList.as_view(), name='last-3-days-tasks'),
    path('overdue-tasks', TaskList.as_view(), name='overdue-tasks'),

    path('task/<int:pk>/', detail, name='task'),
    path('task-create/<str:pk>', TaskCreate.as_view(), name='task-create'),
    path('task-delete/<str:pk>/', TaskDelete.as_view(), name='task-delete'),
    
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]
