import os
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.utils.translation import gettext_lazy as _

try:
    from allauth.account import app_settings as allauth_account_settings
    from allauth.account.adapter import get_adapter
    from allauth.socialaccount.models import EmailAddress
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")


class RegisterSerializerCustom(RegisterSerializer):
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and EmailAddress.objects.is_verified(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."),
                )
            else:
                query = EmailAddress.objects.filter(email__iexact=email)
                if query.exists():
                    email_address = query.first()
                    if email_address.user.has_usable_password():
                        raise serializers.ValidationError(
                            _(
                                "A user is already registered with this e-mail address but hasn't verified their email yet."
                            ),
                        )
        return email


class CustomUserDetailsSerializer(UserDetailsSerializer):

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "user_image",
            "gender",
            "id",
            "is_admin",
        )

    def update(self, instance, validated_data):
        if "user_image" in validated_data:
            old_image_path = instance.user_image.path
            os.remove(old_image_path)

        instance.user_image = validated_data.get("user_image", instance.user_image)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.is_admin = validated_data.get("is_admin", instance.is_admin)
        instance.save()
        return instance
