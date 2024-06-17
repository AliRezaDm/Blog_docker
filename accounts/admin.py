from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import Customuser_changeform, Customuser_creationform
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class CustomAdmin(UserAdmin):

    list_display = ['username', 'password', 'phone' ]
    add_form = Customuser_creationform
    form =  Customuser_changeform


