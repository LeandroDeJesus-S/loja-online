from django import forms
from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _


class CustomSignupForm(SignupForm):
    """override the django allauth form class to make
    first_name and last_name fields required.
    """
    first_name = forms.CharField(required=True, label=_('First name'))
    last_name = forms.CharField(required=True, label=_('Surname'))
