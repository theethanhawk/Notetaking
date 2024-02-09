"""Defines URL patterns for notes_app"""

from django.urls import path
from . import views

app_name = 'notes_app'
urlpatterns = [
    # Home Page showing all entries, navbar at top of page
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


    # Page to edit an existing entry
    # path('entry/<int:pk>/edit/', views.entry_update, name='entry_update'),
    # # Page to delete and entry
    # path('entry/<int:pk>/delete/', views.entry_delete, name='entry_delete'),
]