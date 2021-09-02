from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.registration, name='registration'),
    path('logout', views.logout_view, name='logout'),
    path('post', views.post, name='post'),
    path("subscribe", views.subscribe, name="subscribe"),
    path("edit_critical/<int:review_id>", views.edit_critical, name="edit_critical"),
    path("edit_ticket/<int:ticket_id>", views.edit_ticket, name="edit_ticket"),
    path("flux", views.flux, name="flux"),
    path("ticket_respond/<int:id>", views.ticket_respond, name="ticket_respond"),
]
