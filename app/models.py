from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.dispatch import receiver


class User(AbstractUser):
    """Расширение встроенной модели USER"""
    code = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # class Meta:
    #     swappable = 'AUTH_USER_MODEL'

    def save(self, *args, **kwargs):
        """Права суперюзеру без регистрации"""
        if self.is_superuser: self.is_active=True
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Category(models.Model):
    """Категория"""
    name = models.CharField(max_length=100, default='Без категории')
    subscribers = models.ManyToManyField(User, related_name='subscribed_category', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Publication(models.Model):
    """Публикация"""

    CATEGORY_LIST = (
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('merchant', 'Торговцы'),
        ('gildmasters', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
        ('unknown', 'Без категории')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='publications')
    name = models.CharField(max_length=68)
    title = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='uploads/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def get_absolute_url(self):
        return reverse('publication_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class Notification(models.Model):
    """Уведомление"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Response(models.Model):
    """Отклик"""

    RESPONSE_LIST = (
        ('pending', 'отправлено'),
        ('accepted', 'принято'),
    )

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    status = models.CharField(max_length=20, choices=RESPONSE_LIST, default='отправлено')
    text = models.TextField()
    message = models.CharField(max_length=168)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self):
        return f'{self.author.username} оставил(а) отклик на {self.publication.name}'

class PublicationCategory(models.Model):
    """Промежуточная таблица"""
    publicationThrough = models.ForeignKey(Publication, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)



class OneTimeCode(models.Model):
    """Одноразовый код подтверждения аккаунта при регистрации"""
    value = models.CharField(max_length=5)


@receiver(post_save, sender=Response)
def send_response_notification(sender, instance, created, **kwargs):
    if created:
        publication = instance.publication
        recipient = publication.author.email
        send_mail(
            'Новый отклик на Вашу публикацию',
            f'''Новый отклик на публикацию "{publication.name[:10]}" \n
Текст: {publication.title}''',
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
        )

