from rest_framework import serializers
from core_apps.todo.models import TodoTasks


class TodoTaskSerializer(serializers.ModelSerializer):
    """Serializer for Todo Tasks"""

    class Meta:
        model = TodoTasks
        fields = [
            "id",
            "pkid",
            "title",
            "description",
            "is_completed",
            "created_at",
            "updated_at",
        ]
