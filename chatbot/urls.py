# chatbot/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chatbot_view, name='chatbot_view'),
]
