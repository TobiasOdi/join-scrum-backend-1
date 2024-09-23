from django.contrib import admin
from main.models import UserAccount, PwResetTimestamp
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserAccountInLine(admin.StackedInline):
    model = UserAccount
    can_delete = False
    verbose_name_plural = "Accounts"

class CustomizedUserAdmin(UserAdmin):
    inlines = (UserAccountInLine, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(UserAccount)
admin.site.register(PwResetTimestamp)
