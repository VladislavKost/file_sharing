from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.models import CustomUser
from .serializers import FilesStoreSerializer
from .models import FileStore
from rest_framework.response import Response
from django.http import HttpResponse
import os


def get_owner(data):
    result = []
    for item in data:
        owner_data = get_owner_data(item["owner_id"])
        item["owner"] = owner_data
        del item["owner_id"]
        result.append(item)
    return result


def get_owner_data(owner_id):
    owner = CustomUser.objects.get(id=owner_id)
    owner_data = {
        "id": owner.id,
        "first_name": owner.first_name,
        "last_name": owner.last_name,
    }
    return owner_data


class FilesStoreView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FilesStoreSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        files = FileStore.objects.filter(owner_id=user.id)
        serializer = self.serializer_class(files, many=True)
        response_data = get_owner(serializer.data)

        return Response(response_data)

    def post(self, request, *args, **kwargs):
        user = request.user.id
        request_data = request.data
        request_data["owner_id"] = user
        serializer = self.serializer_class(
            data=request_data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=201)


class FileStoreView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FilesStoreSerializer

    def get(self, request, id, *args, **kwargs):
        user_id = request.user.id
        file_store = FileStore.objects.get(id=int(id))
        if file_store:
            if file_store.owner_id.id == user_id:
                file_path = file_store.file.path
                filename = os.path.basename(file_path)
                file_data = open(file_path, "rb")
                content_type = "application/octet-stream"
                response = HttpResponse(file_data, content_type=content_type)
                response["Content-Disposition"] = f"attachment; filename={filename}"
                return response
            else:
                return Response(
                    {"message": "You are not authorized to view this file"}, status=403
                )
        else:
            return Response({"message": "File not found"}, status=404)

    def delete(self, request, id, *args, **kwargs):
        user_id = request.user.id
        file_store = FileStore.objects.get(id=int(id))
        if file_store and file_store.owner_id.id == user_id:
            file_path = file_store.file.path
            file_store.delete()

            if os.path.exists(file_path):
                os.remove(file_path)

            return Response({"message": "File deleted successfully"}, status=204)
        elif file_store and file_store.owner_id.id != user_id:
            return Response(
                {"message": "You are not authorized to delete this file"}, status=403
            )
        else:
            return Response({"message": "File not found"}, status=404)

    def patch(self, request, id, *args, **kwargs):
        file = FileStore.objects.get(id=id)
        if file.owner_id.id == request.user.id:
            serializer = FilesStoreSerializer(file, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response(self.serializer_class.errors, status=400)


class FilesStoreAllView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FilesStoreSerializer

    def get(self, request, *args, **kwargs):
        files = FileStore.objects.all()
        serializer = self.serializer_class(files, many=True)
        response_data = get_owner(serializer.data)

        return Response(response_data)
