from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import FilesStoreSerializer
from .models import FileStore
from rest_framework.response import Response
from django.http import HttpResponse
import os


class FilesStoreView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FilesStoreSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        files = FileStore.objects.filter(owner_id=user.id)
        serializer = self.serializer_class(files, many=True)
        return Response(serializer.data)

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
            file_store.delete()
            return Response({"message": "File deleted successfully"}, status=204)
        elif file_store and file_store.owner_id.id != user_id:
            return Response(
                {"message": "You are not authorized to delete this file"}, status=403
            )
        else:
            return Response({"message": "File not found"}, status=404)
