from django.urls import path, include
from .views import *

urlpatterns = [
    path('', PublicationList.as_view(), name='publication_list'),
    path('create/', PublicationCreate.as_view(), name='publication_create'),
    path('<int:pk>/', PublicationDetail.as_view(), name='publication_detail'),
    path('<int:pk>/update/', PublicationUpdate.as_view(), name='publication_update'),
    path('<int:pk>/delete/', PublicationDelete.as_view(), name='publication_delete'),
    path('response/<int:pk>delete/', ResponseDelete.as_view(), name='response_delete'),
    path('responses/', response_list, name='response_list'),
    path('responses/delete/<int:publication_id>/', delete_response, name='delete_response'),
    path('responses/accept/<int:publication_id>/', accept_response, name='accept_response'),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile', ProfileView.as_view(), name='profile'),
]