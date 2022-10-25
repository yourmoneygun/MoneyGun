from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms

from main import models  # noqa


# Create your forms here.


# Registration Form
class RegistrationUserForm(UserCreationForm):

    class Meta:
        model = models.User
        fields = ['email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'max_length': 200,
                    'help_text': "Registration without email is not possible!"
                }
            )
        }


# Registration Form
class RegistrationUserReferralLinkForm(UserCreationForm):

    class Meta:
        model = models.User
        fields = ['email', 'password1', 'password2', 'referral_link_main_user']
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'max_length': 200,
                    'help_text': "Registration without email is not possible!"
                }
            )
        }


# Create Transaction User Form
class TransactionUserForm(ModelForm):

    class Meta:
        model = models.Transaction
        fields = ['money', 'wallet']


# U Transaction User Form
class UpdateTransactionUserForm(ModelForm):

    class Meta:
        model = models.Transaction
        fields = ['money']
