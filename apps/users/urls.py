from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('staff/<int:staff_id>/', views.staff_detail, name='staff_detail'),
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/<int:staff_id>/delete/', views.delete_staff, name='delete_staff'),
    path('profile/', views.profile, name='profile'),
]