from django.urls import path
from . import views

urlpatterns = [
    path('studyhub/book/', views.create_booking, name='create_booking'),
] 