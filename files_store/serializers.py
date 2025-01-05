from datetime import datetime
from rest_framework import serializers
from .models import FileStore


class FilesStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileStore
        fields = [
            "id",
            "file",
            "owner_id",
            "file_name",
            "unique_code",
            "uploaded_at",
            "comment",
        ]

    def create(self, validated_data):
        file_name = validated_data["file"].name
        unique_code = self.generate_unique_code(validated_data["owner_id"])
        validated_data["unique_code"] = unique_code
        validated_data["file_name"] = file_name

        file_store_instance = FileStore.objects.create(**validated_data)
        return file_store_instance

    def generate_unique_code(self, owner_id):
        current_time = datetime.now().timestamp()
        return f"CODE-{owner_id.id}-{int(current_time)}"
