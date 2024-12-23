from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import FileStoreSerializer
from .models import FileStore
from rest_framework.response import Response


class FilesStoreView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileStoreSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        files = FileStore.objects.filter(owner_id=user.id)
        serializer = self.serializer_class(files, many=True)
        response_data = serializer.data
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=201)
