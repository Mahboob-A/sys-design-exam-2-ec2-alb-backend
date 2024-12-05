from rest_framework import serializers
from core_apps.todo.models import TodoTasks


# class TodoTaskSerializer(serializers.ModelSerializer):
#     """Serializer for Todo Tasks"""

#     host_with_port = serializers.CharField()
#     host = serializers.CharField()

#     class Meta:
#         model = TodoTasks
#         fields = [
#             "id",
#             "pkid",
#             "title",
#             "description",
#             "is_completed",
#             "created_at",
#             "updated_at",
#         ]


class TodoTaskSerializer(serializers.ModelSerializer):
    """Serializer for Todo Tasks"""

    host = serializers.SerializerMethodField()

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
            "host",
        ]
        
    def get_host(self, obj):
        return self.context.get("host")
