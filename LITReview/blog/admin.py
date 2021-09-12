from .models import User, Ticket, UserFollows, Review
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


# Register your models here

admin.site.register(User, UserAdmin)
admin.site.register(UserFollows)
admin.site.register(Ticket)
admin.site.register(Review)
