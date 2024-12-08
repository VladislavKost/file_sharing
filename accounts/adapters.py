from django.conf import settings
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapterCustom(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return settings.FRONTEND_URL + "/registration/account-email-verify/{}".format(
            emailconfirmation.key
        )
