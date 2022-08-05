from django.urls import path
from viewer import views

urlpatterns = [
    path('', views.main, name='main'),
]
