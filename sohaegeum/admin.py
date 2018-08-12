from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .forms import SohaeUserCreationForm, SohaeUserChangeForm
from .models import SohaeUser

class SohaeUserAdmin(UserAdmin):
    add_form = SohaeUserCreationForm
    form = SohaeUserChangeForm
    model = SohaeUser
    list_display = ['email', 'username', 'name', 'role']

admin.site.register(SohaeUser, SohaeUserAdmin)