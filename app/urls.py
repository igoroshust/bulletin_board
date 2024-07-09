from django.urls import path, include
from .views import *

urlpatterns = [
    path('', PublicationList.as_view(), name='publication_list'),
    path('create/', PublicationCreate.as_view(), name='publication_create'),
    path('<int:pk>/', PublicationDetail.as_view(), name='publication_detail'),
    path('<int:pk>/update/', PublicationUpdate.as_view(), name='publication_update'),
    path('<int:pk>/delete/', PublicationDelete.as_view(), name='publication_delete'),
]