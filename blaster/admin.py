from django.contrib import admin
from django.urls import path, include
from blaster.models import User

from django.contrib.auth.admin import UserAdmin

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)


urlpatters = [
    path('admin/',admin.site.urls),
    path('', include("blaster.urls"))
]
