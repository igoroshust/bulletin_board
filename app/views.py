from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView, DeleteView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import *
from .forms import PubForm

class PublicationList(ListView):
    """Список публикаций"""
    model = Publication
    ordering = '-date'
    template_name = 'app/publications.html'
    context_object_name = 'publications'

class PublicationDetail(DetailView):
    """Содержимое публикации"""
    model = Publication
    template_name = 'app/pub.html'
    context_object_name = 'publication'
    queryset = Publication.objects.all()

class PublicationCreate(CreateView):
    """Создание новой статьи"""
    model = Publication
    form_class = PubForm
    template_name = 'app/pub_create.html'

class PublicationUpdate(UpdateView):
    """Изменение статьи"""
    model = Publication
    form_class = PubForm
    template_name = 'app/pub_update.html'


class PublicationDelete(DeleteView):
    """Удаление статьи"""
    model = Publication
    form_class = PubForm
    template_name = 'app/pub_delete.html'




