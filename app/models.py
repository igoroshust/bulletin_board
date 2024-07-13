from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class User(AbstractUser):
    """Расширение модели USER новым полем code"""
    code = models.CharField(max_length=15, blank=True, null=True)

class Publication(models.Model):
    """Публикация"""

    CATEGORY_LIST = (
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('merchant', 'Торговцы'),
        ('gildmaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
        ('unknown', 'Без категории')
    )

    author = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_LIST, default='unknown')
    name = models.CharField(max_length=68)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    # responses = models.ForeignKey(Response, on_delete=models.CASCADE, null=True) # отклики на статью
    upload = models.FileField(upload_to='uploads/') # файлы

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
class Author(models.Model):
    """Автор"""
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE) # связь один-к-одному со встроенной моделью юзер
    # responses = models.ForeignKey(Response, on_delete=models.CASCADE, null=True) # отклики автора
    # publications = models.ForeignKey(Publication, on_delete=models.CASCADE) # публикации автора
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0, 'Возраст больше 0!')])
    email = models.EmailField()

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Category(models.Model):
    """Категория"""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class PublicationCategory(models.Model):
    """Промежуточная таблица"""
    publicationThrough = models.ForeignKey(Publication, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Response(models.Model):
    """Отклик"""

    author = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

class OneTimeCode(models.Model):
    value = models.CharField(max_length=5)
