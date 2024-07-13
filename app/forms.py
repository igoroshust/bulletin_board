from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from allauth.account.forms import SignupForm
from string import hexdigits
import random

from .models import *

class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user

class PubForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = [
            'name',
            'text',
            'category',
        ]

        # def clean(self):
        #     cleaned_data = super().clean()
        #     name = cleaned_data.get("name")
        #     category = cleaned_data.get("category")
        #     date = cleaned_data.get("date")
        #
        #     if name == category:
        #         raise ValidationError(
        #             "Описание не должно совпадать и именем категории"
        #         )
        #
        #     return cleaned_data