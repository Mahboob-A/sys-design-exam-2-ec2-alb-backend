from django.urls import path

from core_apps.todo.views import TodoAPIView 

urlpatterns = [
    path("task/", TodoAPIView.as_view(), name="todo-api"),
    path("task/<str:task_id>/", TodoAPIView.as_view(), name="todo-api")
]
