from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator


def send_confirmation_mail(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    confirmation_link = reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
    confirmation_url = f"http://{settings.DOMAIN_NAME}{confirmation_link}"
    subject = 'Confirm your registration'
    message = render_to_string('registration/confirmation_email.html', {
        'user': user,
        'confirmation_url': confirmation_url,
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def send_notification_email(user_email, publication_name, accepted=False, deleted=False):
    if accepted:
        subject = 'Ваш отклик принят'
        message = f'Ваш отклик на объявление "{publication_name[:10]}" был принят.'

    elif deleted:
        subject = 'Ваш отклик отклонён'
        message = f'Ваш отклик на объявление "{publication_name[:10]}" был отклонён.'

    else:
        subject = 'Новый отклик на ваше объявление'
        message = f'Вы получили новый отклик на ваше объявление "{publication_name[:10]}...".'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)