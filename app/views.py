from random import random, randint
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView, View)
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages

from .models import *
from .forms import PubForm
from .utils import *

# User = get_user_model()
#
# def send_response_notification_email(response):
#     subject = 'Новый отклик на публикацю'
#     message = 'У Вас новый отклик на публикацию, перейдите в профиль для подробной информации'
#     html_message = render_to_string('response_email.html', {'response': response})
#     recipient_list = [response.ad.author.email]
#     send_mail(subject, message, None, recipient_list, html_message=html_message)

class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'app/invalid_code.html')
        return redirect('http://127.0.0.1:8000/publications/')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'app/profile.html'


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

class PublicationCreate(LoginRequiredMixin, CreateView):
    """Создание новой статьи"""
    raise_exception = True
    permission_required = ('app.add_publication',)
    model = Publication
    form_class = PubForm
    template_name = 'app/pub_create.html'

    def form_valid(self, form):
        """Присваиваем author_id значение юзера"""
        p = form.save(commit=False)
        p.author = self.request.user
        return super().form_valid(form)

class PublicationUpdate(LoginRequiredMixin, UpdateView):
    """Изменение статьи"""
    raise_exception = True
    permission_required = ('app.change_publication', )
    model = Publication
    form_class = PubForm
    template_name = 'app/pub_update.html'


class PublicationDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление статьи"""
    permission_required = ('app.delete_publication',)
    model = Publication
    template_name = 'app/pub_delete.html'
    success_url = reverse_lazy('publication_list')

class CategoryListView(PublicationList):
    model = Category
    template_name = 'app/publications.html'
    context_object_name = 'categories'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk']) # id - поле, по которому хотим отфильтровать объект модели
        queryset = Publication.objects.filter(category=self.category).order_by('-date') # -created_at
        return queryset


class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    fields = ['text']
    template_name = 'responses/create.html'

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     form.instance.publication = get_object_or_404(Publication, pk=self.kwargs['publication_id'])
    #     return super().form_valid(form)

    def form_valid(self, form):
        """Присваиваем author_id значение юзера"""
        p = form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.publication = get_object_or_404(Publication, pk=self.kwargs['publication_id'])
        p.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('publication_detail', kwargs={'pk': self.kwargs['publication_id']})

class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    fields = ['title']
    success_url = reverse_lazy('publication_list')

    def get_queryset(self):
        return Response.objects.filter(publication__author=self.request.user)


def usual_login_view(request):
    """Проверка существования пользователя и корректность пароля"""
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        OneTimeCode.objects.create(code=random.choice('abcde'), user=user)
        # login(request, user)
    else:
        pass

def login_with_code_view(request):
    """Логиним пользователя"""
    username = request.POST['username']
    code = request.POST['code']
    if OneTimeCode.objects.filter(code=code, user__username=username).exists():
        login(request, username) # user
    else:
        pass

def img(request):
    data = Publication.objects.all()
    return render(request, 'app/pub.html', {'data': data})

@login_required
def response_list(request):
    responses = Response.objects.filter(author=request.user) #user=request.user
    return render(request, 'responses/response_list.html', {'responses': responses})

@login_required
def delete_response(request, publication_id):
    response = get_object_or_404(Response, pk=publication_id)
    if response.publication.author != request.user:
        messages.error(request, 'Вы не имеете права удалять этот отклик.')
        return redirect('response_list')
    response.status = 'deleted'
    response.delete()
    send_notification_email(response.author.email, response.publication.title, deleted=True)
    messages.success(request, 'Отклик удален.')
    return redirect('response_list')

@login_required
def accept_response(request, publication_id):
    response = get_object_or_404(Response, pk=publication_id)
    if response.publication.author != request.user:
        messages.error(request, 'Вы не имеете права принимать этот отклик.')
        return redirect('publication_list')
    response.status = 'accepted'
    response.save()
    send_notification_email(response.author.email, response.publication.title, accepted=True)
    messages.success(request, 'Отклик принят.')
    return redirect('publication_list')

