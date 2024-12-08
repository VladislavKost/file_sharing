from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
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
