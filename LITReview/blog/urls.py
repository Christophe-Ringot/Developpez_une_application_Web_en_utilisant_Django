from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("create_review/", views.create_review, name="create_review"),
    path("reply/<int:id>/", views.reply, name="reply"),
    path("flux/", views.flux, name="flux"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("update_review/<int:review_id>/", views.update_review,
         name="update_review"),
    path("delete_review/<int:review_id>/", views.delete_review,
         name="delete_review"),
    path("update_ticket/<int:ticket_id>/", views.update_ticket,
         name="update_ticket"),
    path("delete_ticket/<int:ticket_id>/", views.delete_ticket,
         name="delete_ticket"),
    path("posts/", views.posts, name="posts"),
    path("create_ticket/", views.create_ticket, name="create_ticket"),
    path("subscribe/add_user_follow/", views.add_user_follow,
         name="add_user_follow"),
    path("subscribe/remove_user_follow/", views.remove_user_follow,
         name="remove_user_follow"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
