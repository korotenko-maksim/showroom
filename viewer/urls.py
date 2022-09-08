from django.urls import path, re_path
from viewer import views

urlpatterns = [
    re_path(r'^(?:(?P<categoryId>\d+))?$', views.main, name='main'),
]
