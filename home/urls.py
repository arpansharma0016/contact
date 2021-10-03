from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('', views.index, name="index"),
    path('save_contact/', views.save_contact, name="save_contact"),
    path('delete_contact-<int:id>/', views.delete_contact, name="delete_contact"),
    path('edit_contact-<int:id>/', views.edit_contact, name="edit_contact"),
    path('edit-<int:id>/', views.edit, name="edit"),
    path('search-<int:page>/', views.search, name="search"),
]
