from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Эл.почта')
    first_name = forms.CharField(label='Имя')
    second_name = forms.CharField(label='Фамилия')
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль')
    password_approve = forms.CharField(label='Подтверждение пароля')

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'second_name',
            'password', 'password_approve',
        ),


class CustomSignUpForm(SignUpForm):
    def save(self, request):
        user = super().save(request)

        send_mail(
            subject='Добро пожаловать!',
            message=f'{user.username}, Вы успешно зарегистрированы!',
            from_email=None,
            recipient_list=[user.email],
        )

        return user