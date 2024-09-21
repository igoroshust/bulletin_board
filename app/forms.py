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
        count = random.randint(1000, 9999)
        code = ''.join(str(count))
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
            'title',
            'category',
            'image',
            'wrapper',
            # 'video_url',
        ]
        labels = {
            'name': 'Название',
            'title': 'Текст',
            'category': 'Категория',
            'image': 'Изображение',
            'wrapper': 'Обложка',
            # 'video_url': 'Видео (ссылка)',
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        text = cleaned_data.get('title')
        category = cleaned_data.get('category')
        image = cleaned_data.get('image')
        wrapper = cleaned_data.get('wrapper')

        if name == category:
            raise ValidationError(
                "Описание не должно совпадать с именем категории"
            )

        return cleaned_data

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = {
            'status',
        }