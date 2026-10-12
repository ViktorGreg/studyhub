from django.urls import path
from . import views

urlpatterns = [
  path('studyhub/book/', views.create_booking, name='create_booking'),
  path('studyhub/session/start/', views.start_session, name='start_session'),
  path('studyhub/session/finish/', views.finish_session, name='finish_session'),
  path('studyhub/settings/', views.update_settings, name='update_settings'),
] 