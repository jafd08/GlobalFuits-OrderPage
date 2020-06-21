from django.contrib import admin
from app_accounts.models import Profile

#https://stackoverflow.com/questions/54490783/how-to-add-new-fields-in-django-user-model

class Perfil_Inline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'


admin.site.register(Profile)