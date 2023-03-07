from django.contrib import admin
from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, note_edit_view

urlpatterns = [
    path('', main_view, name='main'),
    path('registration/', registration_view, name='registration'),
    path('auth/', auth_view, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('notes/add/', note_edit_view, name='note_add'),
    path('notes/<int:id>/', note_edit_view, name='note_edit'),
]