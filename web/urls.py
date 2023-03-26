from django.contrib import admin
from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, note_edit_view, tags_view, tags_delete_view, \
    note_delete_view, analytics_view

urlpatterns = [
    path('', main_view, name='main'),
    path('analytics/', analytics_view, name='analytics'),
    path('registration/', registration_view, name='registration'),
    path('auth/', auth_view, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('notes/add/', note_edit_view, name='note_add'),
    path('notes/<int:id>/', note_edit_view, name='note_edit'),
    path('notes/<int:id>/delete', note_delete_view, name='note_delete'),
    path('tags/', tags_view, name='tags'),
    path('tags/<int:id>/delete/', tags_delete_view, name='tags_delete'),
]