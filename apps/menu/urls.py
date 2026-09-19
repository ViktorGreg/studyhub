from django.urls import path
from . import views

urlpatterns = [
    path('menu/add-category/', views.add_category, name='add_category'),
    path('menu/add-item/', views.add_item, name='add_item'),
    path('menu/edit-item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('menu/delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('menu/delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
]