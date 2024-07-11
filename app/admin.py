from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(Response)