from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


from core_apps.todo.models import TodoTasks
from core_apps.todo.serializers import TodoTaskSerializer
from core_apps.common.utils import get_current_host


class TodoAPIView(APIView):
    """Todo API View

    A Simple Todo App
    """

    permission_classes = [
        AllowAny
    ]  # focus on the functionality rather than authentication as per the exam

    def get(self, request, task_id=None, format=None):

        host = request.get_host()
        if task_id:
            try:
                task = TodoTasks.objects.get(id=task_id)
                serializer = TodoTaskSerializer(task, context={"host": host})
                return Response(
                    {"status": "success", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            except TodoTasks.DoesNotExist:
                return Response(
                    {
                        "status": "error",
                        "message": f"Task not found with the task ID: {task_id}",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            tasks = TodoTasks.objects.all()
            serializer = TodoTaskSerializer(
                tasks, many=True, context={"host": host}
            )
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

    def post(self, request, format=None):
        serializer = TodoTaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": f"Task Created Successfully. ID: {serializer.data['id']}",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, task_id=None, format=None):
        if task_id:
            try:
                task = TodoTasks.objects.get(id=task_id)
                serializer = TodoTaskSerializer(task, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(
                        {
                            "status": "success",
                            "message": f"Task Updated Successfully. ID: {task_id}",
                        },
                        status=status.HTTP_200_OK,
                    )
            except TodoTasks.DoesNotExist:
                return Response(
                    {
                        "status": "error",
                        "message": f"Task not found with the task ID: {task_id}",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"status": "error", "message": "Task ID is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, task_id=None, format=None):
        if task_id:
            try:
                task = TodoTasks.objects.get(id=task_id)
                task.delete()
                return Response(
                    {
                        "status": "success",
                        "message": f"Task Deleted Successfully. ID: {task_id}",
                    },
                    status=status.HTTP_204_NO_CONTENT,
                )
            except TodoTasks.DoesNotExist:
                return Response(
                    {
                        "status": "error",
                        "message": f"Task not found with the task ID: {task_id}",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"status": "error", "message": "Task ID is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
