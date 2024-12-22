from django.conf import settings
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapterCustom(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return settings.FRONTEND_URL + "/registration/account-email-verify/{}".format(
            emailconfirmation.key
        )

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.user_image = data.get("user_image")
        user.gender = data.get("gender")
        user.save()
        return user
