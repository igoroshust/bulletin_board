from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Publication)
admin.site.register(Response)