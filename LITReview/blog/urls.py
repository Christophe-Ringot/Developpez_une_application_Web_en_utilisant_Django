from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.registration, name='registration'),
    path('logout', views.logout_view, name='logout'),
    path('post', views.post, name='post'),
]
