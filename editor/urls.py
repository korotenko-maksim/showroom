from django.urls import path

from editor import views

urlpatterns = [
    path('category', views.editCategory, name='editCategory'),
    path('item', views.editItem, name='editItem'),
]
