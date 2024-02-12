"""Defines URL patterns for notes_app"""

from django.urls import path
from . import views

app_name = 'notes_app'
urlpatterns = [
    # Home view with all of users entries and navbar top of page
    path('', views.home, name='home'),
    # View details of a specific entry
    path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
    # Page to create a new entry
    path('entry/new/', views.entry_create, name='entry_create'),
    # Page for editing an entry
    path('edit_entry/<int:pk>/', views.edit_entry, name='edit_entry'),
    # Profile section of navbar
    path('profile/', views.profile, name='profile'),
    # Search bar on nav
    path('search/', views.search_results, name='search_results'),
    # Delete an entry
    path('entry/delete/<int:pk>/', views.entry_delete, name='entry_delete'),
]