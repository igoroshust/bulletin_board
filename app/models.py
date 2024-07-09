from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

APPEAL = 'AP'
COMPLAINT = 'CP'
CATEGORY_LIST = (
    (APPEAL, 'Обращение'),
    (COMPLAINT, 'Жалоба'),
)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Author(models.Model):
    # authorUser = models.OneToOneField(User, on_delete=models.CASCADE) # связь один-к-одному со встроенной моделью юзер
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0, 'Возраст больше 0!')])
    email = models.EmailField()
    # responses = models.ForeignKey(Response, on_delete=models.CASCADE)

class Publication(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True) # null=True
    category = models.CharField(max_length=2, choices=CATEGORY_LIST, default=APPEAL)
    name = models.CharField(max_length=68)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
   # responses = models.ForeignKey(Response, on_delete=models.CASCADE)

class PublicationCategory(models.Model):
    publicationThrough = models.ForeignKey(Publication, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

