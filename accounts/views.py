from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import CustomUserDetailsSerializer
from dj_rest_auth.views import LoginView
from django.core.files import File
import base64
from django.utils import timezone
from dj_rest_auth.app_settings import api_settings
from rest_framework import status
from .models import CustomUser
from files_store.models import FileStore


def get_base64_image(image):
    with open(image, "rb") as image_file:
        return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"


class CustomUserView(APIView):
    serializer_class = CustomUserDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserDetailsSerializer(request.user)
        data = serializer.data
        if request.user.user_image:
            data["user_image"] = get_base64_image(request.user.user_image.path)
        return Response(data)

    def patch(self, request):
        serializer = CustomUserDetailsSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "Account deleted successfully."})


class CustomUsersView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserDetailsSerializer

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserDetailsSerializer(users, many=True)
        response_data = serializer.data
        for user in response_data:
            user_obj = CustomUser.objects.get(id=user["id"])
            if user_obj.user_image:
                user["user_image"] = get_base64_image(user_obj.user_image.path)
            user_files = FileStore.objects.filter(owner_id=user_obj.id)
            user_files_amount = user_files.count()
            user_files_size = sum(file.file.size for file in user_files)
            user["files_amount"] = user_files_amount
            user["files_size"] = user_files_size
        return Response(response_data)


class CustomLoginView(LoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()

        if api_settings.USE_JWT:
            from rest_framework_simplejwt.settings import (
                api_settings as jwt_settings,
            )

            access_token_expiration = (
                timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
            )
            refresh_token_expiration = (
                timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
            )
            return_expiration_times = api_settings.JWT_AUTH_RETURN_EXPIRATION
            auth_httponly = api_settings.JWT_AUTH_HTTPONLY

            data = {
                "user": self.user,
                "access": self.access_token,
            }

            if not auth_httponly:
                data["refresh"] = self.refresh_token
            else:
                # Wasnt sure if the serializer needed this
                data["refresh"] = ""

            if return_expiration_times:
                data["access_expiration"] = access_token_expiration
                data["refresh_expiration"] = refresh_token_expiration

            serializer = serializer_class(
                instance=data,
                context=self.get_serializer_context(),
            )
        elif self.token:
            serializer = serializer_class(
                instance=self.token,
                context=self.get_serializer_context(),
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        response_data = serializer.data
        if self.user.user_image:
            response_data["user"]["user_image"] = get_base64_image(
                self.user.user_image.path
            )
        response = Response(response_data, status=status.HTTP_200_OK)
        if api_settings.USE_JWT:
            from dj_rest_auth.jwt_auth import set_jwt_cookies

            set_jwt_cookies(response, self.access_token, self.refresh_token)
        return response
