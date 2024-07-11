from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (ListView, DetailView, CreateView, DeleteView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
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

class PublicationCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание новой статьи"""
    raise_exception = True
    permission_required('app.add_publication')
    model = Publication
    form_class = PubForm
    template_name = 'app/pub_create.html'

class PublicationUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Изменение статьи"""
    permission_required('app.change_publication')
    raise_exception = True
    model = Publication
    form_class = PubForm
    template_name = 'app/pub_update.html'


class PublicationDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление статьи"""
    permission_required('app.delete_publication')
    raise_exception = True
    model = Publication
    form_class = PubForm
    template_name = 'app/pub_delete.html'
    success_url = reverse_lazy('publication_list')




