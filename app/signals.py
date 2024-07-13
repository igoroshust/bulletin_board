from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from requests import Response, Request

from .models import *

@receiver(pre_save, sender=Response)
def my_handler(sender, instance, created, **kwargs):
    if instance.status:
        mail = instance.author.email
        send_mail(
            'Subject here',
            'Here is the message',
            'igoroshust@yandex.ru',
            [mail],
            fail_silently=False,
        )
    mail = instance.publication.author.email
    send_mail(
        'Subject here',
        'Here is the message',
        'igoroshust@yandex.ru',
        [mail],
        fail_silently=False,
    )