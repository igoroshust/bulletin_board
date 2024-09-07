from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from requests import Response, Request

from .models import *

# @receiver(post_save, sender=Response)
# def send_response_notification(sender, instance, created, **kwargs):
#     if created:
#         publication = instance.publication
#         recipient = publication.author.email
#         send_mail(
#             'Новый отклик на Вашу публикацию',
#             f'''Новый отклик на публикацию "{publication.name[:10]}" \n
# Текст: {publication.title}''',
#             settings.DEFAULT_FROM_EMAIL,
#             [recipient],
#         )

@receiver(post_save, sender=Response)
def send_response_notification(sender, instance, created, **kwargs):
    if created:
        publication = instance.publication
        email = publication.author.email

        subject = 'Новый отклик на Вашу публикацию'

        # text_content = (
        #     f'Статья: {publication.name} <br>'
        #     f'Дата публикации: {publication.date} <br><br>'
        #     f'Ссылка на статью: http://127.0.0.1:8000'
        # )

        html_content = (
            f'Статья: {publication.name} <br>'
            f'<a href="http://127.0.0.1:8000/{publication.get_absolute_url()}">'
            f'Перейти по ссылке</a>'
        )

        msg = EmailMultiAlternatives(subject=subject, from_email='igoroshust@yandex.ru', to=[email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()



