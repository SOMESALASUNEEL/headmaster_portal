from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('documents/', views.document_list, name='document_list'),
    path('document/<int:pk>/', views.document_detail, name='document_detail'),
    path('document/<int:pk>/download/', views.download_document, name='download_document'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
]